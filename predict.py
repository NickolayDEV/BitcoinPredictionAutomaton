import torch
from aiogram import Bot
from src.model import myLSTM, inverse_transform
import pandas as pd
import asyncio
import joblib
import numpy as np
from src.data_request import get_current_currency
from torch.utils.data import TensorDataset,DataLoader
from dotenv import load_dotenv
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fullGPTPrompts.quiet_whale_generator import generate_market_post
from fullGPTPrompts.educational_post_generator import generate_educational_post
from fullGPTPrompts.historical_post_generator import generate_historical_post
from fullGPTPrompts.fullChatGPTPostGeneration import generate_post
import json
import random

load_dotenv()

device ="cpu"
input_dim = 3
output_dim = 1
hidden_dim = 512
layer_dim = 2
batch_size = 64
dropout = 0.3
n_epochs = 100
learning_rate = 5e-5
weight_decay = 1e-4
model_params = {'input_dim': input_dim,
                'hidden_dim' : hidden_dim,
                'layer_dim' : layer_dim,
                'output_dim' : output_dim,
                'dropout_prob' : dropout,
                'device' : device,}
model = myLSTM(**model_params)
model.load_state_dict(torch.load("artifacts/model2.pth",map_location=torch.device('cpu')))
model.eval()
scaler = joblib.load("artifacts/scaler.joblib")
target_scaler=joblib.load("artifacts/target_scaler.joblib")

def predict():
    df = np.array(get_current_currency()).reshape(1,-1)
    actual_price=np.expm1(df[0,2])
    df=scaler.transform(df)
    input_tensor = torch.Tensor(df)
    input_tensor=TensorDataset(input_tensor)
    input_tensor=DataLoader(input_tensor, batch_size=1, shuffle=False)
    predictions=[]
    with torch.no_grad():
        for batch in input_tensor:
            x=batch[0]
            x=x.unsqueeze(1)
            output=model(x)   
            predictions.append(output.item())
    data_result = inverse_transform(target_scaler, np.array(predictions).reshape(1, -1))
    print(actual_price)
    return [np.expm1(i)- actual_price for i in data_result[0]]


async def send_prediction():
    pred = predict()
    print(pred)
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHANNEL_ID = "@realquietwhale"  # или ID, если канал приватный
    bot = Bot(token=TOKEN)
    if pred[0]>0:
        text = f"🔮 BTC за завтрашний день может вырасти на сумму вплоть до {np.absolute(pred[0]):.1f} USD."
    elif pred[0]==0:
        text = f"🔮 Существенного изменеия в курсе не ожидается."
    elif pred[0]<0:
        text = f"🔮 BTC за завтрашний день может упасть на сумму вплоть до {np.absolute(pred[0]):.1f} USD."
    else:
        return
    await bot.send_message(CHANNEL_ID, text)
    await bot.session.close()
def load_topics(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        topics = json.load(f)
    if not topics:
        raise ValueError(f"Файл {filepath} пуст.")
    return topics
async def scheduled_generate_historical_post():
    topic = random.choice(load_topics("data/historical_topics.json"))
    await generate_historical_post(topic)

async def scheduled_generate_market_post():
    topic = random.choice(load_topics("data/popular_coins.json"))["id"]
    await generate_market_post(topic)

async def scheduled_generate_educational_post():
    topic = random.choice(load_topics("data/educational_topics.json"))
    await generate_educational_post(topic)
async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(send_prediction, 'cron', hour=0, minute=0)
    scheduler.add_job(scheduled_generate_historical_post, 'cron', hour=12, minute=0)
    scheduler.add_job(scheduled_generate_market_post, 'cron', hour=15, minute=0)
    scheduler.add_job(scheduled_generate_educational_post, 'cron', hour=18, minute=0)
    scheduler.add_job(generate_post, 'cron', hour=21, minute=0)
    scheduler.start()
    print("🤖 Бот и планировщик запущены.")
    
    while True:
        await asyncio.sleep(3600)  # держим цикл живым

if __name__ == "__main__":
    asyncio.run(main())
    
