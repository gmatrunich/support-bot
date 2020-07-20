import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import dialogflow_v2 as dialogflow
import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
DF_PROJECT_ID = os.environ['DF_PROJECT_ID']
DF_PROJECT_NUMBER = os.environ['DF_PROJECT_NUMBER']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
DF_SESSION_ID = os.environ['DF_SESSION_ID']
LANGUAGE_CODE = 'ru'


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi!')


def echo(bot, update):
    update.message.reply_text(detect_intent_text(
        DF_PROJECT_ID, DF_SESSION_ID, update.message.text, LANGUAGE_CODE)
    )


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def detect_intent_text(project_id, session_id, text, language_code):

    from google.cloud import storage

    storage_client = storage.Client.from_service_account_json(
        GOOGLE_APPLICATION_CREDENTIALS)
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result.fulfillment_text


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
