import requests
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from aiogram import Bot
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
CHANNEL_ID = "@realquietwhale"

# Получаем данные с CoinGecko
def get_btc_data():
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params)
    data = response.json()
    price = round(data["bitcoin"]["usd"], 2)
    change = round(data["bitcoin"]["usd_24h_change"], 2)
    return price, change

# Генерация текста через GPT
async def generate_post():

    price, change = get_btc_data()
    prompt = prompt = f"""
Цена биткоина сегодня составляет ${price}, изменение за сутки — {change}%.
Поделись спокойным наблюдением за ситуацией на рынке BTC. Можно упомянуть уровни, поведение цены, индикаторы, ончейн-данные или макро-фон. Пиши как опытный трейдер: без шаблонов, без структуры, без заголовков. Просто как если бы ты написал короткий, но вдумчивый пост для коллег.

Не используй шаблоны, не добавляй заключения. Просто мысли по рынку.
"""

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты крипто-аналитик, автор канала Quiet Whale"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    text = response.choices[0].message.content.strip()
    await bot.send_message(CHANNEL_ID, text)

# Основной запуск
if __name__ == "__main__":
    
    post = generate_post()
    print(post)
