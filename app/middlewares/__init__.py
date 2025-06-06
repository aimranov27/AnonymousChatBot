"""Middlewares package"""
from aiogram import Dispatcher
from app.utils.payments import TelegramStars
from sqlalchemy.ext.asyncio import async_sessionmaker

from .user import UserMiddleware
from .callback import CallbackMiddleware
from .subscribe import SubMiddleware
from .session import SessionMiddleware
from .payment import PaymentMiddleware


def setup(dp: Dispatcher, sessionmaker: async_sessionmaker, payment: TelegramStars) -> None:
    """
    Initialises and binds all the middlewares.

    :param Dispatcher dp: Dispatcher (root Router)
    :param async_sessionmaker sessionmaker: Async Sessionmaker
    """

    dp.update.outer_middleware(SessionMiddleware(sessionmaker))
    dp.update.outer_middleware(UserMiddleware())
    dp.message.outer_middleware(SubMiddleware())
    dp.callback_query.outer_middleware(SubMiddleware())
    dp.inline_query.outer_middleware(SubMiddleware())
    dp.callback_query.outer_middleware(CallbackMiddleware())
    dp.update.outer_middleware(PaymentMiddleware(payment))
