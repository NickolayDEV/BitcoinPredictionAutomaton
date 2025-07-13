import os
from openai import AsyncOpenAI
from aiogram import Bot
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = "@realquietwhale"

bot = Bot(token=TELEGRAM_TOKEN)


async def generate_educational_post(topic: str) -> None:
    prompt = f"""
Ты — автор Telegram-канала "Quiet Whale", опытный, спокойный трейдер. Пиши в рассудительном, аналитическом тоне.

Твоя задача — объяснить одну из тем, связанных с криптовалютами или финансовыми рынками, просто и без лишней терминологии. Представь, что тебе пишет младший коллега, интересующийся темой.

Не давай советов и не навязывай мнений. Только факты, логика и лёгкое размышление.

Тема: {topic}

Формат вывода — короткий текст до 800 символов, без заголовка и без хэштегов.
""".strip()

    response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
    text = response.choices[0].message.content.strip()
    await bot.send_message(CHANNEL_ID, text)


if __name__ == "__main__":
    asyncio.run(generate_educational_post("Что такое деривативы на крипторынке?"))