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
        logger.info("TelegramStars payment class initialized")

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
            logger.info(f"Creating payment with params: chat_id={chat_id}, title={title}, amount={amount}, start_param={start_param}")
            
            # Validate parameters
            if not isinstance(amount, int) or amount <= 0:
                raise ValueError(f"Invalid amount: {amount}")
            if not title or not description:
                raise ValueError("Title and description cannot be empty")
            if not payload:
                raise ValueError("Payload cannot be empty")
                
            # Create the invoice
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
            logger.info(f"Payment created successfully for chat_id={chat_id}")
        except ValueError as e:
            logger.error('Invalid payment parameters: %s', str(e))
            raise
        except Exception as exc:
            logger.error('Failed to create Telegram Stars payment: %s', str(exc), exc_info=True)
            raise

    async def check_payment(self, payment_id: str) -> CheckResponse:
        """Check payment status"""
        try:
            logger.info(f"Checking payment status for payment_id={payment_id}")
            # Get payment status from Telegram
            payment = await self.bot.get_payment(payment_id)
            logger.info(f"Payment status: {payment.status}, amount: {payment.total_amount}")
            return CheckResponse(
                is_paid=payment.status == "paid",
                amount=payment.total_amount,  # Convert from cents
            )
        except Exception as exc:
            logger.error('Failed to check Telegram Stars payment: %s', str(exc), exc_info=True)
            return CheckResponse(False)
