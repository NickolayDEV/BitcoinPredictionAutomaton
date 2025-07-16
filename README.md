# Bitcoin Price Predictor Bot
A Telegram-ready project that predicts the next day's Bitcoin price using historical data and machine learning.
It also integrates with GPT to generate text-based posts and insights.

In addition, the project includes a fully deployed Telegram bot that runs in real time to automate market analysis, educational content, and BTC price forecasts for the channel [@realquietwhale](https://t.me/realquietwhale).
Posts are scheduled and generated daily using AI and up-to-date financial data.
---

## Features

- 📊 Daily Bitcoin price prediction
- 🤖 GPT-powered post generation
- 📡 Telegram bot integration (optional)
- 🧠 Trained ML model with preprocessing pipeline

---

## Tech Stack

- Python 3.10
- Pandas, Scikit-Learn
- Pytorch
- Jupyter
- OpenAI API
- Docker
## Instalation
> git clone https://github.com/NickolayDEV/botforbitcoinprediction.git
> cd bitcoin-predictor
> pip install -r requirements.txt
## Project Structure
```
├── artifacts/                # Trained model and scalers
├── fullGPTPrompts/           # Receiving posts from GPT
├── src/                      # Core codebase
├── predict.py                # Entry-point to start the bot and make predictions
├── .env                      # API keys, configs (excluded from Git)
├── data/raw/btc-usd-max.csv  # Raw historical BTC price data
├── modeltrain.ipynb          # Jupyter notebook demonstrating EDA and model training
```