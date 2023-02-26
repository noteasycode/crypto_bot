# Binance Crypto Bot
Telegram bot for assisting in cryptocurrency trading on Binance.
Displays current cryptocurrency price. Predicts price movement up or down in the next 30 minutes.

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