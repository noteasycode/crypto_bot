# Binance Crypto Bot
Telegram bot for assisting in cryptocurrency trading on Binance.
Displays current cryptocurrency price. Predicts price movement up or down in the next 30 minutes.
The prediction function performs technical analysis based on the closing prices of the past 9 
and 21 candle periods, and determines the probability of a price change up or down. This forecast is 
valid for the next 30 minutes after receiving the data, as the function retrieves data at 30-minute 
intervals (30-minute klines). For better forecast accuracy, longer-term data and other time intervals 
can be used. However, it should be noted that predictions in financial markets are never entirely 
accurate, as markets can move unexpectedly.

## Requirements:
```
Python 3.7
```

## Instructions for running (via GitHub):

Clone a repository and navigate to it in the command line:

```sh
git clone https://github.com/noteasycode/crypto_bot.git
```

```sh
cd crypto_bot
```
Create a .env file inside the crypto_bot directory.
Example .env file:

```sh
BINANCE_API_KEY='YOUR_TELEGRAM_BOT_TOKEN'
BINANCE_SECRET_KEY='YOUR_TELEGRAM_BOT_TOKEN'
TELEGRAM_BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
```

Create and activate a virtual environment:

```sh
python3 -m venv env
```

```sh
source env/bin/activate
```

```sh
python3 -m pip install --upgrade pip
```

Install dependencies from the requirements.txt file:

```sh
pip install -r requirements.txt
```

Run the project:

```sh
python3 manin.py
```