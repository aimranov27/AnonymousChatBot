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


async def show_profile(message: types.Message, user: User) -> None:
    """Show profile handler"""
    vip_status = 'yox'
    if user.is_vip:
        remaining_days = (user.vip_time - datetime.now()).days
        vip_status = f'var ({remaining_days} gün qalıb)'
    
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
        await call.message.edit_text(
            texts.user.PROFILE % (
                escape(call.from_user.full_name),
                ('Kişi' if user.is_man else 'Qadın'),
                user.age,
                ('var' if user.is_vip else 'yox')
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
