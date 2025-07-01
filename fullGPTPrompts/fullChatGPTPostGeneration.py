import requests
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
def generate_post(price, change):
    prompt = f"""
Ты автор Telegram-канала "Quiet Whale". Напиши аналитический пост по биткоину, используя следующие данные:

- Текущая цена BTC: ${price}
- Изменение за 24ч: {change}%
- Добавь рассуждения про уровни поддержки/сопротивления, RSI, ончейн-активность (примерно, как если бы ты смотрел на график).
- Можешь упомянуть фонды, доллар или макро-фон, если уместно.
- Тон: спокойный, аналитический. Без призывов, без рекомендаций. Просто наблюдение.
- Структура:
  1. Заголовок (1 строка)
  2. Основной текст (3–4 абзаца)
  3. Финальный вывод — как сценарий

Пиши так, как будто ты опытный, но рассудительный трейдер.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты крипто-аналитик, автор канала Quiet Whale"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

# Основной запуск
if __name__ == "__main__":
    price, change = get_btc_data()
    print(price,change)
    post = generate_post(price, change)
    print(post)
