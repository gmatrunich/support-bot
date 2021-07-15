import tg_logger
import df_api
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import os


logger = logging.getLogger('telegram_logger')


def start(bot, update):
    update.message.reply_text('Hi!')


def send_answer(bot, update):
    has_answer, bot_answer = df_api.detect_intent_text(update.message.text)
    update.message.reply_text(bot_answer)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    telegram_bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
    logger.setLevel(logging.WARNING)
    logger.addHandler(tg_logger.TGLogsHandler(
        telegram_bot,
        os.environ['TELEGRAM_CHAT_ID'])
    )

    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, send_answer))
    dp.add_error_handler(error)

    try:
        updater.start_polling()
        updater.idle()
    except requests.exceptions.HTTPError as err:
        logger.warning(f'Something has gone wrong!\n{err}')
