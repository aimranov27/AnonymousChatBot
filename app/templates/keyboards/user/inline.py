"""User inline keyboards"""
from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prices import VIP_OPTIONS
from app.database.models import Sponsor, Room


def split(items: list, size: int) -> list[list]:
    """Split items into chunks"""
    return [
        items[index:index + size]
        for index in range(0, len(items), size)
    ]


def subscription(sponsors: list[Sponsor]) -> InlineKeyboardMarkup:
    """Subscription keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            *(
                [
                    InlineKeyboardButton(
                        text=sponsor.title,
                        url=sponsor.link,
                    ),
                ] for sponsor in sponsors
            ),
            [
                InlineKeyboardButton(
                    text='Проверить подписку',
                    callback_data='checksub',
                ),
            ],
        ]
    )

BUY = InlineKeyboardMarkup(
    inline_keyboard=[
        *(
            [
                InlineKeyboardButton(
                    text=item['name'],
                    callback_data='buy:stars:%s' % key,
                ),
            ] for key, item in VIP_OPTIONS.items()
        ),
        [
            InlineKeyboardButton(
                text='Pulsuz əldə et 🤫',
                callback_data='ref',
            ),
        ],
    ],
)

ADULT_GENDER = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Kişi ♂️',
                callback_data='adult:male',
            ),
            InlineKeyboardButton(
                text='Qadın ♀️',
                callback_data='adult:female',
            ),
        ]
    ],
)

BACK_VIP = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Geri 🔙',
                callback_data='back:vip',
            ),
        ],
    ],
)

PROFILE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Cinsi dəyiş👩‍❤️‍👨',
                callback_data='edit:gender',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Yaşı dəyiş📝',
                callback_data='edit:age',
            ),
        ],
    ],
)

GENDER = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Kişi🙋‍♂',
                callback_data='gender:1',
            ),
            InlineKeyboardButton(
                text='Qadın🙎‍♀',
                callback_data='gender:0',
            ),
        ],
    ],
)

SHOW_CONTACTS = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Показать',
                callback_data='show:contacts',
            ),
        ],
    ],
)

FRIEND_REQUEST = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Принять✅',
                callback_data='accept:friend',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Отклонить❌',
                callback_data='decline:friend',
            ),
        ],
    ],
)

COMPLAINT = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Göndər✅',
                callback_data='accept:complaint',
            ),
        ],
        [
            InlineKeyboardButton(
                text='Ləğv et❌',
                callback_data='decline:complaint',
            ),
        ],
    ],
)

PRE_CHANGE_NICKNAME = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Сменить никнейм🔄',
                callback_data='change:nickname',
            ),
        ],
    ],
)

def change_nickname(new_nickname: dict) -> InlineKeyboardMarkup:
    """Change nickname keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Подтвердить✅',
                    callback_data='accept:change:nickname:%s' % new_nickname,
                )
            ],
            [
                InlineKeyboardButton(
                    text='Отменить❌',
                    callback_data='decline:change:nickname',
                )
            ]
        ]
    )

def room_list(rooms: List[Room]) -> InlineKeyboardMarkup:
    """Room list keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 [%s/%s] %s" % (
                        room.room_online_members,
                        room.room_online_limit
                        if room.room_online_limit != 0 else '∞',
                        room.room_name,
                    ),
                    callback_data='join:room:%i' % room.id,
                )
            ] for room in rooms
        ]
    )
