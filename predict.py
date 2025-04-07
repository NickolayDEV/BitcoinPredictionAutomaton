API_KEY = "REMOVED"
import torch
from aiogram import Bot
from model import myLSTM  # Заменить на твою архитектуру
import pandas as pd
import asyncio
import joblib
import numpy as np
from data_request import get_current_currency
from torch.utils.data import TensorDataset,DataLoader

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
input_dim = 2
output_dim = 1
hidden_dim = 512
layer_dim = 2
batch_size = 64
dropout = 0.3
n_epochs = 200
learning_rate = 5e-5
weight_decay = 1e-4
#Возможно придется перенести модель на CPU
model_params = {'input_dim': input_dim,
                'hidden_dim' : hidden_dim,
                'layer_dim' : layer_dim,
                'output_dim' : output_dim,
                'dropout_prob' : dropout,
                'device' : device}
model = myLSTM(**model_params)
model.load_state_dict(torch.load("model2.pth"))
model=model.to('cuda')
model.eval()
scaler = joblib.load("scaler.joblib")

def predict():
    df = np.array(get_current_currency()).reshape(1,-1)
    print(df)
    df=scaler.transform(df)
    print(df)
    
    input_tensor = torch.Tensor(df)
    input_tensor=TensorDataset(input_tensor)
    input_tensor=DataLoader(input_tensor, batch_size=1, shuffle=False)
    predictions=[]
    with torch.no_grad():
        for batch in input_tensor:
            x=batch[0]
            x=x.unsqueeze(1).to('cuda')
            output=model(x)   
            predictions.append(output.item())
    return predictions

# --- Асинхронная отправка в Telegram ---
#async def send_prediction():
def send_prediction():
    pred = predict()
    TOKEN = "ТВОЙ_ТОКЕН"
    CHANNEL_ID = "@название_канала"  # или ID, если канал приватный
    bot = Bot(token=TOKEN)
    
    text = f"🔮 Прогноз курса BTC на завтра: {pred:.2f} USD"
    #await bot.send_message(CHANNEL_ID, text)
    #await bot.session.close()
send_prediction()
# --- Запуск скрипта ---
#if __name__ == "__main__":
#    asyncio.run(send_prediction())
