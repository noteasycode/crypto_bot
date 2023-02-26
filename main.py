import pandas as pd
import os
import ta
import telegram
import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


load_dotenv()

# Налаштування логера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Отримання API-ключів для Binance та Telegram
binance_api_key = os.getenv('BINANCE_API_KEY')
binance_secret_key = os.getenv('BINANCE_SECRET_KEY')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Створення з'єднання з Binance API
binance_client = Client(api_key=binance_api_key, api_secret=binance_secret_key)

# Створення з'єднання з Telegram API
bot = telegram.Bot(token=telegram_bot_token)
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

supported_symbols = ['BTC', 'BNB', 'ETH', 'SOL']


def start(update, context):
    update.message.reply_text('Привіт! Я бот для допомоги у торгівлі криптовалютами на Binance. '
                              'Використовуйте /help, щоб отримати довідку про доступні команди.')


def help(update, context):
    chat_id = update.effective_chat.id
    message = "Доступні команди:\n\n"
    message += "/start : Запускає бота\n"
    message += "/help : Показує довідку про доступні команди\n"
    message += "/price : Показує поточну ціну на криптовалюту\n"
    message += "/predict : Передбачає рух ціни вгору або вниз на наступні 30 хв."
    context.bot.send_message(chat_id=chat_id, text=message)


def price(update, context):
    if len(context.args) == 0:
        keyboard = [
            [InlineKeyboardButton(symbol, callback_data=f'price-{symbol}')] for symbol in supported_symbols
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Choose a symbol:', reply_markup=reply_markup)
    else:
        symbol = context.args[0].upper()
        if symbol not in supported_symbols:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Sorry, {symbol} is not supported.')
        else:
            try:
                price = binance_client.get_symbol_ticker(symbol=symbol + 'USDT')['price']
                update.callback_query.edit_message_text(f"Current price {symbol}: {float(price):.2f} USDT")
            except BinanceAPIException as e:
                update.callback_query.edit_message_text(f"Failed to get price for {symbol.upper()}: {e}")


def button(update, context):
    query = update.callback_query
    query.answer()
    symbol: str = query.data
    if symbol.startswith('price-'):
        symbol = symbol.lstrip('price-')
        context.args = [symbol]
        price(update, context)
    if symbol.startswith('predict-'):
        symbol = symbol.lstrip('predict-') + 'USDT'
        context.args = [symbol]
        predict(update, context)


def predict(update, context):
    """
    Ця функція здійснює технічний аналіз на основі замикання цін з минулих 9 і 21 періодів свічок,
    і визначає ймовірність зміни ціни вгору або вниз.
    Цей прогноз дійсний на наступні 30 хвилин після отримання даних, оскільки функція отримує дані за 30-хвилинним
    інтервалом (30-minute klines). Для кращої точності прогнозу можна використовувати більш довготривалі дані та
    інші інтервали часу. Однак слід знати, що прогнози на фінансових ринках ніколи не є абсолютно точними,
    оскільки ринки можуть рухатися неочікуваним чином.
    """
    if len(context.args) == 0:
        keyboard = [
            [InlineKeyboardButton(symbol, callback_data=f'predict-{symbol}')] for symbol in supported_symbols
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Choose a symbol:', reply_markup=reply_markup)
    else:
        symbol = context.args[0].upper()
        try:
            candles = binance_client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE)
            closes = [float(candle[4]) for candle in candles]
            current_price = binance_client.get_symbol_ticker(symbol=symbol)['price']
            closes.append(float(current_price))
            series = pd.Series(closes)
            ema_9 = series.ewm(span=9, adjust=False).mean().iloc[-1]
            ema_21 = series.ewm(span=21, adjust=False).mean().iloc[-1]
            if ema_9 > ema_21:
                direction = "вгору"
            else:
                direction = "вниз"
            probability = round(ta.volatility.bollinger_pband(series).iloc[-1] * 100, 2)
            if probability > 50:
                update.callback_query.edit_message_text(
                    f"Ціна {symbol} може піти {direction} з ймовірністю {probability}% (поточна ціна: {current_price})")
            else:
                update.callback_query.edit_message_text(
                    f"Ціна {symbol} може піти {direction}, але ймовірність менша 50% (поточна ціна: {current_price})")

        except BinanceAPIException as e:
            update.callback_query.edit_message_text(f"Не вдалося отримати аналіз для {symbol}: {e}")
        except AttributeError as e:
            update.callback_query.edit_message_text(f"Не вдалося отримати аналіз для {symbol}: {e}")


def main():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('price', price))
    dispatcher.add_handler(CommandHandler('predict', predict))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
