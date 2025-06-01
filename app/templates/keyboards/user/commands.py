"""User commands"""
from aiogram.types import BotCommand


USER_COMMANDS = [
    BotCommand(
        command="search",
        description="🔍 Həmsöhbət axtar",
    ),
    BotCommand(
        command="stop",
        description="🛑 Söhbəti bitir",
    ),
    BotCommand(
        command="next",
        description="🔄 Növbəti həmsöhbət",
    ),
    BotCommand(
        command="profile",
        description="👤 Profil",
    ),
    BotCommand(
        command="vip",
        description="💎 VIP",
    ),
]
