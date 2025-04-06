API_KEY = "REMOVED"
import torch
from aiogram import Bot
from model import myLSTM  # Заменить на твою архитектуру
import pandas as pd
import asyncio
import joblib
# --- Загрузка модели ---
model = myLSTM()
model.load_state_dict(torch.load("model2.pth"))
model.eval()
scaler = joblib.load("scaler.pkl")

def predict():
    df = pd.read_csv("latest_data.csv")  # Или твой способ получения данных
    input_tensor = torch.tensor(df.values).float().unsqueeze(0)
    with torch.no_grad():
        prediction = model(input_tensor).item()
    return prediction

# --- Асинхронная отправка в Telegram ---
async def send_prediction():
    TOKEN = "ТВОЙ_ТОКЕН"
    CHANNEL_ID = "@название_канала"  # или ID, если канал приватный
    bot = Bot(token=TOKEN)
    pred = predict()
    text = f"🔮 Прогноз курса BTC на завтра: {pred:.2f} USD"
    await bot.send_message(CHANNEL_ID, text)
    await bot.session.close()

# --- Запуск скрипта ---
if __name__ == "__main__":
    asyncio.run(send_prediction())
