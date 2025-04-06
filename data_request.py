
from datetime import datetime, timedelta
from dateutil import tz
import requests
API_KEY = "REMOVED"
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
market_cap = data["data"]["BTC"]["quote"]["USD"]["market_cap"]

print(f"💰 Price now: {price}")
print(f"🏦 Market Cap now: {market_cap}")

