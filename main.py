"""Main file for the bot (Webhook version)"""
import os
import time
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from fastapi import FastAPI, Request

from app import middlewares, handlers
from app.database import create_sessionmaker
from app.utils import set_commands, load_config, schedule, payments

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger('aiogram.event').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# App & global variables
app = FastAPI()
bot = None
dp = None
sessionmaker = None
payment = None

# Main initialization function
async def on_startup():
    global bot, dp, sessionmaker, payment

    logger.info("Starting bot...")
    config = load_config()

    os.environ['TZ'] = config.bot.timezone
    time.tzset()
    logger.info(f'Set timezone to "{config.bot.timezone}"')

    # Setup storage
    if config.bot.use_redis:
        storage = RedisStorage.from_url(
            f'redis://{config.redis.host}:6379/{config.redis.db}'
        )
    else:
        storage = MemoryStorage()

    sessionmaker = await create_sessionmaker(config.db)

    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML",
    )

    payment = payments.TelegramStars(bot)

    dp = Dispatcher(storage=storage)
    dp["config"] = config  # 🔥 Store config in dispatcher context
    middlewares.setup(dp, sessionmaker, payment)
    handlers.setup(dp)

    await set_commands(bot, config, sessionmaker)
    await schedule.setup(bot, sessionmaker)

    webhook_url = f"https://{config.bot.domain}/webhook"
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook set: {webhook_url}")


# Shutdown cleanup
async def on_shutdown():
    await bot.delete_webhook()
    await dp.fsm.storage.close()
    logger.info("Bot shutdown complete")

# FastAPI events
@app.on_event("startup")
async def startup_event():
    await on_startup()

@app.on_event("shutdown")
async def shutdown_event():
    await on_shutdown()

# Webhook endpoint
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        logger.info(f"Received webhook update: {update}")
        config = dp["config"]
        logger.info(f"Current config: {config}")
        await dp.feed_update(bot, types.Update(**update))
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
    return {"ok": True}

# Run locally with uvicorn for debugging (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)