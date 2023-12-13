from googletrans import Translator
import requests, datetime
from dir_bot import create_bot


code_to_smaile = {
    'Clear': 'Ясно \U00002600',
    'Clouds': 'Облачно \U00002601',
    'Rain': 'Дождь \U00002614',
    'Drizzle': 'Дождь \U00002614',
    'Thunderstorm': 'Гроза \U000026A1',
    'Snow': 'Снег \U0001F328',
    'Mist': 'Туман \U0001F32B'
}

code_to_concept = {
    0: '\U0001F914',
    1: '\U0001F7E2 \U0001F7E2 \U0001F7E2',
    2: '\U0001F7E2 \U0001F7E1 \U0001F7E2',
    3: '\U0001F7E1 \U0001F7E1 \U0001F7E1',
    4: '\U0001F7E0 \U0001F7E0 \U0001F7E0',
    5: '\U0001F534 \U0001F534 \U0001F534',
}

ret_error_city = f'\U00002620 Проверьте название города \U00002620\n\n' \
                 f'Примеры: \n' \
                 f'Москва (/Moscow)\n' \
                 f'Санкт-Петербург\n' \
                 f'Новосибирск (/Novosibirsk)\n' \
                 f'Екатеринбург (/Yekaterinburg)\n' \
                 f'Казань (/Kazan)\n' \
                 f'Нижний Новгород\n' \
                 f'Челябинск (/Chelyabinsk)\n' \
                 f'Самара (/Samara)\n' \
                 f'Омск (/Omsk)\n' \
                 f'Ростов-на-Дону\n' \
                 f'Уфа (/Ufa)\n' \
                 f'Пермь (/Perm)\n' \
                 f'Красноярск (/Krasnoyarsk)\n' \
                 f'Воронеж (/Voronezh)\n' \
                 f'Волгоград (/Volgograd)\n' \
                 f'Краснодар (/Krasnodar)\n\n' \
                 f'Если название верно, то попробуйте ввести его с большой буквы или на английском!'

def get_weather_name(city, lat=None, lon=None):
    translator = Translator()
    try:
        if city is not None:
            city_en = translator.translate(text=city, dest='en')
            req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_en.text}"
                               f"&appid={create_bot.config['TOKEN']['token_api_weather']}&units=metric").json()
            req_concept = None
        else:
            req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}"
                               f"&appid={create_bot.config['TOKEN']['token_api_weather']}&units=metric").json()
            req_concept = requests.get(f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}"
                                       f"&appid={create_bot.config['TOKEN']['token_api_weather']}&units=metric").json()
        city_name = translator.translate(text=req['name'], src='en', dest='ru')
        if req['weather'][0]['main'] in code_to_smaile:
            weather = code_to_smaile[req['weather'][0]['main']]
        else:
            weather = "Посмотри в окно, не пойму что там за погода!"

        if req_concept is not None and req_concept['list'][0]['main']['aqi'] in code_to_concept:
            concept = code_to_concept[req_concept['list'][0]['main']['aqi']]
        else:
            concept = code_to_concept[0]

        sunrise_timestamp = datetime.datetime.fromtimestamp(req['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(req['sys']['sunset'])
        len_day = datetime.datetime.fromtimestamp(req['sys']['sunset']) - datetime.datetime.fromtimestamp(req['sys']['sunrise'])

        text = f"*** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ***\n" \
               f"Погода в: {city_name.text} {req['sys']['country']}\n" \
               f"{weather}\n" \
               f"Температура: {req['main']['temp']}°C\n" \
               f"Влажность: {req['main']['humidity']}%\n" \
               f"Давление: {req['main']['pressure']} мм.рт.ст\n" \
               f"Скорость ветра: {req['wind']['speed']} м/с\n" \
               f"Качетсво воздуха: {concept}\n" \
               f"Восход солнца: {sunrise_timestamp}\n" \
               f"Закат солнца: {sunset_timestamp}\n" \
               f"Продолжительность дня: {len_day}"
        return text
    except Exception as ex:
        print(ex)
        if city is not None:
            return ret_error_city
        else:
            return f'\U00002620 Не могу найти вашу локацию \U00002620'

