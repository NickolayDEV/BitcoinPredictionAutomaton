
from datetime import datetime, timedelta
from dateutil import tz
import requests
from dotenv import load_dotenv
import os
import numpy as np
load_dotenv()
def get_current_currency():
    API_KEY = os.getenv("COINMARKET_API_KEY")
    symbol = "BTC"

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    params = {
        "symbol": "BTC",
        "convert": "USD"
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    price = data["data"]["BTC"]["quote"]["USD"]["price"]
    volume_24h = data["data"]["BTC"]["quote"]["USD"]["volume_24h"]
    market_cap = data["data"]["BTC"]["quote"]["USD"]["market_cap"]

    return np.log1p(market_cap),np.log1p(volume_24h),np.log1p(price)

