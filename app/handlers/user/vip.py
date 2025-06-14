"""VIP handlers"""

import logging
from aiogram import Router, types, F
from aiogram.filters import Text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from prices import VIP_OPTIONS
from app.filters import IsVip
from app.templates import texts
from app.templates.keyboards import user as nav
from app.utils.payments import TelegramStars
from app.database.models import User, Bill


logger = logging.getLogger('vip')


async def vip_menu(update: types.Message | types.CallbackQuery) -> None:
    """VIP menu"""
    if isinstance(update, types.CallbackQuery):
        update = update.message

    elif update.text in ('K axtar 👨', 'Q axtar 👩'):
        await update.answer('VIP abunəliyinizin müddəti başa çatıb.')

    await update.answer(
        texts.user.VIP,
        reply_markup=nav.inline.BUY,
    )


async def create_stars_payment(call: types.CallbackQuery, payment: TelegramStars) -> None:
    """Create Stars payment"""
    try:
        item_id = call.data.split(':')[-1]
        if item_id not in VIP_OPTIONS:
            logger.error(f"Invalid item_id in callback data: {call.data}")
            await call.answer("Invalid item selected. Please try again.", show_alert=True)
            return

        item = VIP_OPTIONS[item_id]
        logger.info(f"Creating payment for item: {item_id}, user: {call.from_user.id}")
        logger.info(f"Payment details: days={item['days']}, stars={item['starPrice']}")

        await payment.create_payment(
            chat_id=call.message.chat.id,
            title=f"VIP abunə",
            description=f"{item['days']} günlük VIP abunəlik əldə edirsiniz",
            payload=f"vip:{item_id}",
            amount=int(item['starPrice']),
        )
        logger.info(f"Payment created successfully for user {call.from_user.id}")
        await call.message.delete()
    except ValueError as e:
        logger.error(f"Invalid payment parameters: {str(e)}")
        await call.answer("Invalid payment parameters. Please try again.", show_alert=True)
    except Exception as e:
        logger.error(f"Payment creation failed: {str(e)}", exc_info=True)
        await call.answer("Ödəniş yaratmaq alınmadı. Lütfən, yenidən cəhd edin.", show_alert=True)


async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, payment: TelegramStars) -> None:
    """Handle pre-checkout query"""
    logger.info(f"[PRE_CHECKOUT] Received pre_checkout_query: {pre_checkout_query}")
    logger.info(f"[PRE_CHECKOUT] Payment payload: {pre_checkout_query.invoice_payload}")
    logger.info(f"[PRE_CHECKOUT] User: {pre_checkout_query.from_user.id}")
    logger.info(f"[PRE_CHECKOUT] Amount: {pre_checkout_query.total_amount}")
    
    try:
        # Verify the payment payload
        if not pre_checkout_query.invoice_payload.startswith("vip:"):
            logger.error(f"Invalid payment payload: {pre_checkout_query.invoice_payload}")
            await pre_checkout_query.answer(
                ok=False,
                error_message="Yanlış ödəniş yükü. Yenidən cəhd edin."
            )
            return

        # Verify the item exists
        item_id = pre_checkout_query.invoice_payload.split(':')[1]
        if item_id not in VIP_OPTIONS:
            logger.error(f"Invalid item_id in pre-checkout: {item_id}")
            await pre_checkout_query.answer(
                ok=False,
                error_message="Yanlış abunə seçimi. Yenidən cəhd edin."
            )
            return

        # Accept the payment
        logger.info(f"[PRE_CHECKOUT] Accepting payment for user {pre_checkout_query.from_user.id}")
        await pre_checkout_query.answer(ok=True)
    except Exception as e:
        logger.error(f"Pre-checkout error: {str(e)}", exc_info=True)
        await pre_checkout_query.answer(
            ok=False,
            error_message="Ödəniş təsdiq edilməmişdir. Yenidən cəhd edin."
        )


async def successful_payment(message: types.Message, session: AsyncSession, payment: TelegramStars) -> None:
    """Handle successful payment"""
    try:
        logger.info(f"[PAYMENT] Processing successful payment for user {message.from_user.id}")
        logger.info(f"[PAYMENT] Payment details: {message.successful_payment}")
        
        # Extract item_id from payload
        item_id = message.successful_payment.invoice_payload.split(':')[1]
        if item_id not in VIP_OPTIONS:
            raise ValueError(f"Invalid item_id: {item_id}")

        item = VIP_OPTIONS[item_id]
        logger.info(f"[PAYMENT] Item details: {item}")

        # Get user
        user = await session.scalar(
            select(User)
            .where(User.id == message.from_user.id)
        )
        if not user:
            raise ValueError(f"İstifadəçi tapılmadı: {message.from_user.id}")

        # Add VIP
        user.add_vip(item['days'])
        logger.info(f"[PAYMENT] Added {item['days']} days of VIP to user {user.id}")

        # Record payment
        session.add(
            Bill(
                id=message.successful_payment.telegram_payment_charge_id,
                user_id=user.id,
                amount=message.successful_payment.total_amount,
                ref=user.ref,
            )
        )
        await session.commit()
        logger.info(f"[PAYMENT] Payment recorded in database for user {user.id}")

        # Send confirmation
        await message.answer(
            f'<i>Təbrik edirik, siz {item["days"]} günlük VIP statusunu əldə etdiniz!</>',
            reply_markup=nav.reply.main_menu(user),
        )
        logger.info(f"[PAYMENT] Confirmation sent to user {user.id}")
    except Exception as e:
        logger.error(f"Ödənişin işlənmə xətası: {str(e)}", exc_info=True)
        await message.answer(
            "Uğursuz ödəniş. Dəstək xidməti ilə əlaqə saxlayın və kodu bildirin: " + 
            message.successful_payment.telegram_payment_charge_id
        )


async def back_bill(call: types.CallbackQuery) -> None:
    """Back bill"""
    await call.message.edit_text(
        texts.user.VIP,
        reply_markup=nav.inline.BUY,
    )


async def referral(
    call: types.CallbackQuery, user: User, bot_info: types.User,
) -> None:
    """Referral"""
    await call.message.edit_text(
        texts.user.REF % (
            user.invited,
            bot_info.username,
            user.id,
        ),
        reply_markup=nav.inline.BACK_VIP,
        disable_web_page_preview=True,
    )


def register(router: Router) -> None:
    """Register handlers"""
    router.message.register(vip_menu, Text(
        [
            'K axtar 👨',
            'Q axtar 👩',
            '18+ çat 🔞',
            'Cinsəl axtarış ♂️',
            # 'Комнаты 🏠',
        ]
    ), IsVip(False))

    router.message.register(vip_menu, Text('VIP 👑'))
    router.callback_query.register(vip_menu, Text('vip'))
    router.callback_query.register(create_stars_payment, Text(startswith='buy:stars'))
    router.callback_query.register(back_bill, Text('back:vip'))
    router.callback_query.register(referral, Text('ref'))

    # Register payment handlers
    router.pre_checkout_query.register(pre_checkout_query)
    router.message.register(successful_payment, F.successful_payment)
