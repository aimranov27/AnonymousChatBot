"""Payments utils"""
import logging
from dataclasses import dataclass
from aiogram import Bot
from aiogram.types import LabeledPrice


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
            # Create a valid start_parameter by removing any invalid characters
            start_param = f"vip_{payload.replace(':', '_')}"
            
            await self.bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token="",  # Empty for Telegram Stars
                currency="XTR",  # Telegram Stars currency
                prices=[LabeledPrice(label=title, amount=amount)],  # Price in stars
                start_parameter=start_param,  # Valid format: starts with letter, only letters/numbers/underscores
            )
        except Exception as exc:
            logger.error('Failed to create Telegram Stars payment: %s', str(exc))
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
