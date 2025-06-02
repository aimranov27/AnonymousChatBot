from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.client.bot import Bot
from typing import Any, Awaitable, Callable, Dict
from app.utils.payments import TelegramStars
import logging

logger = logging.getLogger(__name__)

class PaymentMiddleware(BaseMiddleware):
    """
    Middleware to inject the payment object into handler context.
    """

    def __init__(self, payment: TelegramStars):
        self.payment = payment
        logger.info("PaymentMiddleware initialized")

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        logger.info("PaymentMiddleware called")
        data["payment"] = self.payment
        logger.info("Payment object injected into data")
        return await handler(event, data)