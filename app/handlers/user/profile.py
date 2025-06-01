"""Profile handlers"""
from contextlib import suppress

from aiogram import Router, types
from aiogram.filters import Command, Text, StateFilter
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.templates import texts
from app.templates.keyboards import user as nav
from app.database.models import User, Bill
from app.utils.text import escape
from app.utils.payments import BasePayment


async def show_profile(message: types.Message, user: User) -> None:
    """Show profile handler"""
    await message.answer(
        texts.user.PROFILE % (
            escape(message.from_user.full_name),
            ('Kişi' if user.is_man else 'Qadın'),
            user.age,
            ('var' if user.is_vip else 'yox'),
            user.balance

        ),
        reply_markup=nav.inline.PROFILE,
    )


async def pre_edit_profile(
    call: types.CallbackQuery, state: FSMContext
) -> bool | None:
    """Pre edit profile handler"""
    action = call.data.split(':')[1]

    if action == 'age':
        await call.message.edit_text('<i>Neçə yaşın var?</>')
        await state.set_state('edit.age')

    else:
        await call.message.edit_text(
            '<i>Cins:</>',
            reply_markup=nav.inline.GENDER,
        )


async def edit_gender(
    call: types.CallbackQuery,
    user: User,
    state: FSMContext,
    session: AsyncSession
) -> bool | None:
    """Edit gender handler"""
    user.is_man = bool(int(call.data.split(':')[1]))
    await session.commit()

    if not user.age:
        with suppress(TelegramAPIError):
            await call.message.edit_text(
                '<i>Yaşınızı daxil edin (16-dan 99-da qədər)</i>'
            )

        await state.set_state('edit.age')
    else:
        await call.message.edit_text(
            texts.user.PROFILE % (
                escape(call.from_user.full_name),
                ('Kişi' if user.is_man else 'Qadın'),
                user.age,
                ('var' if user.is_vip else 'yox'),
                user.balance,
            ),
            reply_markup=nav.inline.PROFILE,
        )


async def edit_age(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession,
    user: User
) -> bool | None:
    """Edit age handler"""
    try:
        age = int(message.text)
        if age < 16 or age > 99:
            raise ValueError

    except ValueError:
        return await message.answer('<i>Düzgün yaş daxil edin.</>')

    prev_age = user.age
    user.age = age
    await session.commit()
    await state.clear()

    if not prev_age:
        return await message.answer(
            texts.user.START,
            reply_markup=nav.reply.main_menu(user),
        )

    await show_profile(message, user)


async def pre_top_up_balance(
    call: types.CallbackQuery, state: FSMContext
) -> bool | None:
    """Pre top up balance handler"""
    with suppress(TelegramAPIError):
        await call.message.edit_text(
            '<i>Balansınızı nə qədər artırmaq istərdiniz?</i>'
        )
    await state.set_state('add.balance')


async def top_up_balance(
    message: types.Message,
    state: FSMContext,
    payment: BasePayment
) -> bool | None:
    """Top up balance handler"""
    try:
        amount: int = int(message.text)
    except ValueError:
        return await message.answer('<i>Məbləği rəqəm olaraq daxil edin.</>')

    if amount < 1:
        return await message.answer('<i>Məbləğ sıfırdan yüksək olmalıdır.</>')

    await state.clear()
    bill = await payment.create_payment(amount)
    await message.answer(
        texts.user.TOP_UP_BALANCE % (amount),
        reply_markup=nav.inline.bill(bill, amount, is_vip=False),
    )


async def check_bill(
    call: types.CallbackQuery,
    session: AsyncSession,
    user: User,
    payment: BasePayment
) -> bool | None:
    """Check bill handler"""
    bill_id, item_id = call.data.split(':')[2:]
    bill_status = await payment.check_payment(int(bill_id))

    if not bill_status.is_paid:
        return await call.answer('Uğursuz ödəniş❗', True)

    bill = await session.scalar(
        select(Bill)
        .where(Bill.id == int(bill_id))
    )

    if bill:
        return await call.answer('Hesab köhnəlmişdir ⏲️', True)

    user.balance += int(item_id)
    session.add(
        Bill(
            id=int(bill_id),
            user_id=user.id,
            amount=bill_status.amount,
            ref=user.ref,
        )
    )
    await session.commit()

    await call.message.delete()
    await call.message.answer(
        '<i>💰 Balansınız %i ₼ məbləğində artırılmışdır </>' % (int(item_id)),
    )


async def back_bill(call: types.CallbackQuery, user: User) -> None:
    """Back bill handler"""
    await call.message.edit_text(
        texts.user.PROFILE % (
            escape(call.from_user.full_name),
            ('Kişi' if user.is_man else 'Qadın'),
            user.age,
            ('var' if user.is_vip else 'yox'),
            user.balance,
        ),
        reply_markup=nav.inline.PROFILE,
    )


def register(router: Router) -> None:
    """Register handlers"""
    router.message.register(show_profile, Command('profile'))
    router.message.register(show_profile, Text('Profil 👤'))
    router.callback_query.register(pre_edit_profile, Text(startswith='edit:'))
    router.callback_query.register(pre_top_up_balance, Text('add:balance'))
    router.callback_query.register(back_bill, Text('back:profile'))
    router.callback_query.register(
        check_bill, Text(startswith='check:profile:')
    )
    router.message.register(top_up_balance, StateFilter('add.balance'))
    router.callback_query.register(edit_gender, Text(startswith='gender:'))
    router.message.register(edit_age, StateFilter('edit.age'))
