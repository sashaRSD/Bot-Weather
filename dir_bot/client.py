from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from dir_weather import get
from dir_bot import create_bot
dp = create_bot.dp
bot = create_bot.bot

donat = ['/Поддержать']
contact = ['/Обратная_связь']
kb_client = ReplyKeyboardMarkup(resize_keyboard=True).add(*contact).insert(*donat)


@dp.message_handler(commands=['start'])
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, f'Добрый день, {message.from_user.first_name}!\n')
        await bot.send_message(message.from_user.id, f'Бот рассказывает о погоде!\n'
                                                     f'Для этого отправьте местоположение или введите город ;)')
        await bot.send_message(message.from_user.id, f'Города, которые состоят из 1 слова - можно ввести на английском языке, '
                                                     f'начаиная с символа "/" ,тогда можно запросить прогноз погоды в нем - по нажатию на него!\n'
                                                     f'Пример: Москва или /Moscow', reply_markup=kb_client)
    except:
        await message.delete()
        await message.reply('Напишите мне в личные сообщения')


@dp.message_handler(commands=['help'])
async def commands_help(message: types.Message):
    await bot.send_message(message.from_user.id, f'Отправьте местоположение или введите город ;)\n\n'
                                                 f'Примеры: \n'
                                                 f'Москва (/Moscow)\n'
                                                 f'Санкт-Петербург\n'
                                                 f'Новосибирск (/Novosibirsk)\n'
                                                 f'Екатеринбург (/Yekaterinburg)\n'
                                                 f'Казань (/Kazan)\n'
                                                 f'Нижний Новгород\n'
                                                 f'Челябинск (/Chelyabinsk)\n'
                                                 f'Самара (/Samara)\n'
                                                 f'Омск (/Omsk)\n'
                                                 f'Ростов-на-Дону\n'
                                                 f'Уфа (/Ufa)\n'
                                                 f'Пермь (/Perm)\n'
                                                 f'Красноярск (/Krasnoyarsk)\n'
                                                 f'Воронеж (/Voronezh)\n'
                                                 f'Волгоград (/Volgograd)\n'
                                                 f'Краснодар (/Krasnodar)', reply_markup=kb_client)


@dp.message_handler(content_types=["location"])
async def location(message):
    text = get.get_weather_name(None, message.location.latitude, message.location.longitude)
    await bot.send_message(message.from_user.id, text, reply_markup=kb_client)


@dp.message_handler(commands=['Поддержать'])
async def commands_donat(message: types.Message):
    text = 'Жми сюда!'
    url = 'https://www.tinkoff.ru/cf/71ARxuIBdob'
    url_button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=text, url=url))
    await message.answer('Поддержать автора копейкой ;)', reply_markup=url_button)


@dp.message_handler(commands=['Обратная_связь'])
async def commands_contact(message: types.Message):
    await message.answer('Наши контактные данные: \n'
                         'Электронная почта - kaa.1999@mail.ru \n'
                         'Username Telegram - @sasha_rsd')


@dp.message_handler()
async def city(message: types.Message):
    if message.text.startswith('/'):
        city = message.text[1:]
    else:
        city = message.text
    text = get.get_weather_name(city)
    await bot.send_message(message.from_user.id, text, reply_markup=kb_client)


