"""User texts"""

START = '''
🏠 Əsas menyu:
'''

REG_GENDER = '''
<b>📝 Регистрация</>
👣 Шаг 1 из 2

<i>Выбери ниже, какого ты пола?</>
'''
REG_AGE = '''
<b>📝 Регистрация</>
👣 Шаг 2 из 2

<i>Напиши, cколько тебе лет? (от 10 до 99)</>
'''

NOT_SUBBED = '''
<i><b>✅Чтобы пользоваться ботом, вы должны подписаться на наши каналы</b>

Подпишиcь и нажми «Продолжить»!</i>
'''

DEFAULT_VIP = 'Bu funksiya yalnız VIP istifadəçilər üçün əlçatandır'

VIP = '''
<b>👑 VIP statusun üstünlükləri:</>

<i>🔎 - Cinslə axtarış
🔞 - 18+ çat
❌ - Reklamsız
🖼 - Media paylaşımı (şəkillər, videolar, giflər, stikerlər)</>
'''

BILL = '''
⭐️ Чтобы получить доступ к VIP - подписке, оплатите счёт ниже ⬇️ 

• <i>После оплаты нажмите на кнопку "Проверить"</i> ✅
'''

REF = '''
<i>Dəvət linkini dostlarınla bölüş və hər qoşulan üçüncü dostun üçün 1 günlük </> <b>👑 VIP statusu</> <i>qazan!</>

<b>Dəvət olunub:</> <code>%i</>

Sənin şəxsi dəvət linkin:
👉  https://t.me/%s?start=%i
'''

PROFILE = '''
<b>👤 Profil</>

<b>💬 Ad -</b> %s
<b>👫 Cins -</b> %s
<b>🔞 Yaş -</b> %s
<b>👑 VIP -</b> %s
'''

SEARCH_END = '''
<i>Axtarış dayandırıldı
Növbəti həmsöhbəti tapmaq üçün - /next
</>
'''

DIALOGUE_END_SELF = '''
<i>Siz söhbəti bitirdiniz 🙄
Növbəti həmsöhbəti tapmaq üçün - /next
</>
'''

DIALOGUE_END = '''
<i>Qarşı tərəf sizinlə əlaqəni kəsdi 😞
Növbəti həmsöhbəti tapmaq üçün - /next
</>
'''
DIALOGUE_SEARCH = '''
<i>🔎 Həmsöhbət axtarılır...</>
'''
DIALOGUE_GENDER = '<i>Həmsöhbətin cinsini seçin! ❤️‍🔥</>'
DIALOGUE_FOUND = '''
<b>Həmsöhbət tapıldı! 🎁</>

<i>Növbəti həmsöhbəti tapmaq üçün - /next
Çatı bitirmək üçün - /stop</>
'''
DIALOGUE_FRIEND = '''
<b>Диалог с другом создан! 👥 </>

<i>Для прекращения диалога - /stop</>
'''
BANNED = '<b>⛔️ Sizin hesab bloklanmışdır.</>'

NO_ACTIVE_CHAT = '''
<i>Sizin aktiv çatınız yoxdur 🤔
Yeni çat başlatmaq üçün - /search</>
'''

PRE_SHOW_CONTACTS = '''
<b>📱 Показать контакты</>

Стоимость услуги: %i ₽
Ваш Баланс: %i ₽
'''
SHOW_CONTACTS = '''
💬 Имя: %s
💬 Фамилия: %s
🔗 %s: %s

'''
ADD_FRIEND_REQUEST = '''
<b>📩 Запрос в друзья отправлен!</>
'''

ADD_FRIEND_REQUEST_SECOND = '''
<b>👥 Ваш собеседник хочет добавить вас в друзья</>
'''
MY_FRIENDS = '''
<b>👥 Мои друзья - %s</>

🟢 - Доступен
🔴 - Не доступен (заблокировал бота)
🟡 - В диалоге
'''

FRIEND_INFO = ''' 
👥 Мой друг [%s]:

<b>💬 Имя -</b> %s
<b>👫 Пол -</b> %s
<b>🔞 Возраст -</b> %s
<b>👑 VIP -</b> %s
'''
FRIEND_DIALOGUE_REQUEST = '''
👥 Ваш друг %s хочет вас пригласить в диалог!
'''


PRE_COMPLAINT = '''
<b>❗️ Şikayətinizi qeyd edin</>
<i>Bu mesajı qarşı tərəf görməyəcək</>
'''


VIEW_COMPLAINT = '''
<b>❗️ Şikayət</>
Səbəb: <i>%s</>
'''


COMPLAINT = '''
<b>❗️ Жалоба на пользователя</>

<b>ID Диалога:</b> %s
<b>Потерпевший:</b> %s
<b>Обвиняемый:</b> %s

<b>Причина:</b> <i>%s</>
'''

JOIN_ROOM = '''
<b>🏠 Вход в комнату [%s]</>
<b>👤 Никнейм:</b> %s
<b>👤 Участников:</b> %s

<i>/leave - покинуть комнату 🚪</>
<i>/members - посмотреть участников 👤</>
'''

DEFAULT_COMMAND_RESPONSE = '''
<i>Həmsöhbət tapmaq üçün /search istifadə edin.</>
'''

PRE_ROOM_CHANGE_NICKNAME = '''
<b>🏠 Комната:</b> %s

<b>👤 Ваш Никнейм:</b> %s

Стоимость услуги: %i ₽
Ваш Баланс: %i ₽
'''
ROOM_CHANGE_NICKNAME = '''
<b>🏠 Комната:</b> %s

<b>👤 Ваш Никнейм:</b> %s
<b>👤 Новый Никнейм:</b> %s

Стоимость услуги: %i ₽
Ваш Баланс: %i ₽
'''
