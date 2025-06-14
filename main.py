"""Main file for the bot (Webhook version)"""
import os
import time
import logging
from datetime import datetime
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

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
bot: Optional[Bot] = None
dp: Optional[Dispatcher] = None
sessionmaker = None
payment = None
is_ready = False

# Main initialization function
async def on_startup():
    global bot, dp, sessionmaker, payment, is_ready

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
    await bot.set_webhook(
        webhook_url,
        allowed_updates=[
            "message",
            "edited_message",
            "callback_query",
            "message_reaction",
            "message_reaction_count",
            "pre_checkout_query",
            "successful_payment"
        ]
    )
    logger.info(f"Webhook set: {webhook_url}")
    
    is_ready = True
    logger.info("Bot startup complete and ready to handle requests")


# Shutdown cleanup
async def on_shutdown():
    global is_ready
    is_ready = False
    
    if bot:
        await bot.delete_webhook()
    if dp:
        await dp.fsm.storage.close()
    logger.info("Bot shutdown complete")

# FastAPI events
@app.on_event("startup")
async def startup_event():
    await on_startup()

@app.on_event("shutdown")
async def shutdown_event():
    await on_shutdown()

# Health check endpoint
@app.get("/health")
async def health_check():
    if not is_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready"}
        )
    return {"status": "healthy"}

# Webhook endpoint
@app.post("/webhook")
async def telegram_webhook(request: Request):
    if not is_ready:
        logger.warning("Received webhook request while bot is not ready")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready"}
        )
        
    start_time = time.time()
    request_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{int(start_time * 1000)}"
    logger.info(f"[{request_id}] Webhook request received at {datetime.now().isoformat()}")
    
    try:
        # Parse the update
        update = await request.json()
        parse_time = time.time() - start_time
        logger.info(f"[{request_id}] Update parsed in {parse_time:.3f}s")
        
        # Log update type and details
        update_type = update.get('message', {}).get('text') or update.get('callback_query', {}).get('data') or update.get('pre_checkout_query', {}).get('invoice_payload') or 'unknown'
        logger.info(f"[{request_id}] Update type: {update_type}")
        
        # Process the update
        process_start = time.time()
        config = dp["config"]
        logger.info(f"[{request_id}] Starting update processing")
        
        await dp.feed_update(bot, types.Update(**update))
        process_time = time.time() - process_start
        logger.info(f"[{request_id}] Update processed in {process_time:.3f}s")
        
        # Calculate total time
        total_time = time.time() - start_time
        logger.info(f"[{request_id}] Total webhook processing time: {total_time:.3f}s")
        
        if total_time > 5:  # Warning if processing takes more than 5 seconds
            logger.warning(f"[{request_id}] Webhook processing took longer than 5 seconds!")
            
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"[{request_id}] Webhook processing error after {error_time:.3f}s: {str(e)}", exc_info=True)
    return {"ok": True}

# Run locally with uvicorn for debugging (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)