"""Payments utils"""
import logging
from dataclasses import dataclass
from aiogram import Bot
from aiogram.types import LabeledPrice
import time


@dataclass
class CheckResponse:
    """Check response class"""
    is_paid: bool
    amount: int = 0


logger = logging.getLogger('payments')

class TelegramStars:
    """Telegram Stars payment class"""

    def __init__(self, bot: Bot) -> None:
        """Initialize the Telegram Stars payment class"""
        self.bot = bot

    async def create_payment(
        self,
        chat_id: int,
        title: str,
        description: str,
        payload: str,
        amount: int,
    ) -> None:
        """Create payment using Telegram Stars"""
        try:
            # Validate amount
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")

            # Create a valid start_parameter
            # Remove any non-alphanumeric characters except underscore
            safe_payload = ''.join(c for c in payload if c.isalnum() or c == '_')
            # Ensure it starts with a letter
            if not safe_payload[0].isalpha():
                safe_payload = 'p_' + safe_payload
            # Add timestamp to ensure uniqueness
            start_param = f"vip_{safe_payload}_{int(time.time())}"
            
            logger.info(f"Creating payment with params: chat_id={chat_id}, title={title}, amount={amount}, start_param={start_param}")
            
            await self.bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token="",  # Empty for Telegram Stars
                currency="XTR",  # Telegram Stars currency
                prices=[LabeledPrice(label=title, amount=amount)],  # Price in stars
                start_parameter=start_param,
            )
            logger.info(f"Payment created successfully for chat_id={chat_id}")
        except Exception as exc:
            logger.error('Failed to create Telegram Stars payment: %s', str(exc), exc_info=True)
            raise

    async def check_payment(self, payment_id: str) -> CheckResponse:
        """Check payment status"""
        try:
            # Get payment status from Telegram
            payment = await self.bot.get_payment(payment_id)
            return CheckResponse(
                is_paid=payment.status == "paid",
                amount=payment.total_amount,  # Convert from cents
            )
        except Exception as exc:
            logger.error('Failed to check Telegram Stars payment: %s', str(exc))
            return CheckResponse(False)
