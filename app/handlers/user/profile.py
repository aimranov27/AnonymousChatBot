"""Profile handlers"""
from contextlib import suppress
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command, Text, StateFilter
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.templates import texts
from app.templates.keyboards import user as nav
from app.database.models import User
from app.utils.text import escape


def get_vip_status(user: User) -> str:
    """Calculate VIP status string with days remaining"""
    if not user.is_vip:
        return 'yox'
        
    time_remaining = user.vip_time - datetime.now()
    remaining_days = time_remaining.days
    # Show at least 1 day if there's any time remaining
    if remaining_days == 0 and time_remaining.total_seconds() > 0:
        remaining_days = 1
    return f'var ({remaining_days} gün qalıb)'


async def show_profile(message: types.Message, user: User) -> None:
    """Show profile handler"""
    vip_status = get_vip_status(user)
    
    await message.answer(
        texts.user.PROFILE % (
            escape(message.from_user.full_name),
            ('Kişi' if user.is_man else 'Qadın'),
            user.age,
            vip_status
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
        # Use the helper function to get VIP status
        vip_status = get_vip_status(user)
            
        await call.message.edit_text(
            texts.user.PROFILE % (
                escape(call.from_user.full_name),
                ('Kişi' if user.is_man else 'Qadın'),
                user.age,
                vip_status
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


def register(router: Router) -> None:
    """Register handlers"""
    router.message.register(show_profile, Command('profile'))
    router.message.register(show_profile, Text('Profil 👤'))
    router.callback_query.register(pre_edit_profile, Text(startswith='edit:'))
    router.callback_query.register(edit_gender, Text(startswith='gender:'))
    router.message.register(edit_age, StateFilter('edit.age'))
