from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@realquietwhale"

bot = Bot(token=TOKEN,  default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
async def generate_historical_post(topic: str) -> str:
    prompt = f"""
Ты — автор Telegram-канала "Quiet Whale", спокойный и наблюдательный трейдер с многолетним опытом. Пиши вдумчиво, аналитически, без навязывания мнений и без резких оценок.

Расскажи кратко об одном значимом событии, тренде или инструменте в истории криптовалют или глобальных финансов. Суть — показать, *что произошло*, *почему это имело значение* и *чему это могло научить рынок*.

Избегай перегрузки датами и именами — цель не академичность, а ясность и контекст. Пиши так, чтобы даже новичок почувствовал важность момента. Без заголовков, хэштегов и выводов. Просто короткий, цельный рассказ.

Тема: {topic}

Вывод — короткий текст до 800 символов, с лёгким использованием Markdown (жирный текст, курсив).
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
