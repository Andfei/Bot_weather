import requests
import datetime
from config import bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message:types.message):
    await message.reply("Hello!")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = weather.json()
        city = data['name']
        weather = data['main']['temp']
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        weather_max = data['main']['temp_max']
        weather_min = data['main']['temp_min']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        speed_wind = data['wind']['speed']

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Город: {city}\n"
              f"Температура:\nСредняя:{weather}°C Максимальная: {weather_max}°C Минимальная: {weather_min}°C {wd} \n"
              f"Влажность: {humidity}\n"
              f"Давление: {pressure}\n"
              f"Скорость ветра: {speed_wind}\nХорошего дня!")
    except:
        await message.reply("Проверьте название города")
if __name__ == '__main__':
    executor.start_polling(dp)