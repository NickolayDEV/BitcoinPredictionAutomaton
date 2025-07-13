from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from aiogram import Bot
import asyncio
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@realquietwhale"

bot = Bot(token=TOKEN)
async def generate_historical_post(topic: str) -> str:
    prompt = f"""
Ты — автор Telegram-канала "Quiet Whale", опытный трейдер и наблюдатель за финансовыми рынками. Пиши спокойно, без оценок, без рекомендаций.

Твоя задача — рассказать краткую историю одного события, тренда или инструмента в крипте или мире финансов. Пост не должен быть длинным — достаточно, чтобы читатель увидел картину в целом.

Фактология важна, но перегружать датами не нужно. Главное — логика и понимание, почему это событие было важным.

Тема: {topic}

Формат вывода — короткий текст до 800 символов, без заголовка и без хэштегов.
"""
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    text = response.choices[0].message.content.strip()
    await bot.send_message(CHANNEL_ID, text)
