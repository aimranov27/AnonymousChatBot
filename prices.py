"""Settings for the bot"""
VIP_OPTIONS = {
    'day': {
        'name': '1 gün - 30 ⭐ / 1 ₼',
        'price': 1,
        'starPrice': 30,
        'days': 1,
    },
    'week': {
        'name': '🔥 1 həftə - 90 ⭐ / 3 ₼',
        'price': 3,
        'starPrice': 90,
        'days': 7,
    },
    'month': {
        'name': '1 ay - 180 ⭐ / 6 ₼',
        'price': 6,
        'starPrice': 180,
        'days': 31,
    },
    'year': {
        'name': '1 il - 365 ⭐ / 12 ₼',
        'price': 12,
        'starPrice': 365,
        'days': 365,
    },
}
SHOW_CONTACTS_PRICE: int = 10  # Цена за показ контактов
CHANGE_NICKNAME_IN_ROOM_PRICE: int = 10  # Цена за смену никнейма в комнате
