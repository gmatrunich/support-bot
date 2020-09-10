from base import TelegramLogsHandler, detect_intent_text
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']


logger = logging.getLogger('telegram_logger')


def start(bot, update):
    update.message.reply_text('Hi!')


def echo(bot, update):
    has_answer, bot_answer = detect_intent_text(update.message.text)
    update.message.reply_text(bot_answer)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    telegram_bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(telegram_bot, TELEGRAM_CHAT_ID))

    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    try:
        updater.start_polling()
        updater.idle()
    except requests.exceptions.HTTPError as err:
        logger.warning(f'Something has gone wrong!\n{err}')
