import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_historical_post(topic: str) -> str:
    prompt = f"""
Ты — автор Telegram-канала "Quiet Whale", опытный трейдер и наблюдатель за финансовыми рынками. Пиши спокойно, без оценок, без рекомендаций.

Твоя задача — рассказать краткую историю одного события, тренда или инструмента в крипте или мире финансов. Пост не должен быть длинным — достаточно, чтобы читатель увидел картину в целом.

Фактология важна, но перегружать датами не нужно. Главное — логика и понимание, почему это событие было важным.

Тема: {topic}

Формат вывода — короткий текст до 800 символов, без заголовка и без хэштегов.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return response['choices'][0]['message']['content'].strip()
