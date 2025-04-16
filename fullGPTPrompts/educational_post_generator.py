import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from aiogram import Bot
import asyncio
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@realquietwhale"

bot = Bot(token=TOKEN)
async def generate_educational_post(topic: str) -> str:
    prompt = f"""
Ты — автор Telegram-канала "Quiet Whale", опытный, спокойный трейдер. Пиши в рассудительном, аналитическом тоне.

Твоя задача — объяснить одну из тем, связанных с криптовалютами или финансовыми рынками, просто и без лишней терминологии. Представь, что тебе пишет младший коллега, интересующийся темой.

Не давай советов и не навязывай мнений. Только факты, логика и лёгкое размышление.

Тема: {topic}

Формат вывода — короткий текст до 800 символов, без заголовка и без хэштегов.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    text=response['choices'][0]['message']['content'].strip()
    await bot.send_message(CHANNEL_ID, text)
