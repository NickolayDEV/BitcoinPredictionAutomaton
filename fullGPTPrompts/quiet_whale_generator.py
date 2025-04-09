from openai import OpenAI
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()



client = OpenAI(api_key = os.getenv("OPENAI_API_KEY")) 

def fetch_coin_data(coin_id: str, vs_currency: str = "usd") -> dict:
    """
    Получает метрики монеты с CoinGecko по coin_id (например, 'bitcoin')
    """
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "ids": coin_id,
        "sparkline": False
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"Coin '{coin_id}' not найден на CoinGecko")

    coin = data[0]

    return {
        "name": coin.get("name"),
        "current_price": coin.get("current_price"),
        "market_cap": coin.get("market_cap"),
        "market_cap_rank": coin.get("market_cap_rank"),
        "fully_diluted_valuation": coin.get("fully_diluted_valuation"),
        "total_volume": coin.get("total_volume"),
        "high_24h": coin.get("high_24h"),
        "low_24h": coin.get("low_24h"),
        "price_change_24h": coin.get("price_change_24h"),
        "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
        "market_cap_change_24h": coin.get("market_cap_change_24h"),
        "market_cap_change_percentage_24h": coin.get("market_cap_change_percentage_24h"),
        "circulating_supply": coin.get("circulating_supply"),
        "total_supply": coin.get("total_supply"),
        "max_supply": coin.get("max_supply"),
        "ath": coin.get("ath"),
        "ath_change_percentage": coin.get("ath_change_percentage"),
        "ath_date": coin.get("ath_date"),
        "atl": coin.get("atl"),
        "atl_change_percentage": coin.get("atl_change_percentage"),
        "atl_date": coin.get("atl_date"),
        "price_change_percentage_1h": coin.get("price_change_percentage_1h_in_currency"),
        "last_updated": coin.get("last_updated")
    }


def generate_market_post(metrics: dict) -> str:
    """
    Генерирует спокойный аналитический пост в стиле Quiet Whale
    на основе рыночных метрик криптовалюты.
    """

    formatted_lines = []
    for key, value in metrics.items():
        if isinstance(value, str):
            formatted_value = f'"{value}"'
        else:
            formatted_value = value
        formatted_lines.append(f'  "{key}": {formatted_value}')
    formatted_metrics = "{\n" + ",\n".join(formatted_lines) + "\n}"


    prompt = f"""
Ты — автор Telegram-канала "Quiet Whale", опытный и спокойный трейдер. Пиши в рассудительном, аналитическом тоне.

Ниже приведён набор актуальных рыночных метрик по криптовалюте. Сформируй короткий пост в телеграм-формате (до 800 символов), в котором ты спокойно, без советов и оценок, поделишься наблюдениями:
— Упомяни текущее положение актива (цена, капитализация, позиция в рейтинге).
— Обрати внимание на динамику за сутки (изменение цены, объёма, капитализации).
— Если заметен контекст (например, цена далека от ATH или, наоборот, подбирается к нему), — мягко отметь это.
— Постарайся выявить, что выглядит особенно интересно (например, волатильность, объёмы, редкость роста при падении рынка и т.д.).
— Никаких призывов к действию, прогнозов или рекомендаций. Только наблюдение.

Формат вывода — короткий, связный текст без заголовков и хэштегов.

Метрики:
```json
{formatted_metrics}
"""
# Запрос в OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ],
        max_tokens=500,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
if __name__ == "__main__":
    print(generate_market_post(fetch_coin_data(coin_id='bitcoin')))