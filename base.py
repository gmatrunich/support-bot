import logging
import os
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv


load_dotenv()
DF_PROJECT_ID = os.environ['DF_PROJECT_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
DF_SESSION_ID = os.environ['DF_SESSION_ID']
LANGUAGE_CODE = 'ru'


class TelegramLogsHandler(logging.Handler):

    def __init__(self, telegram_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.telegram_bot = telegram_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_text(text):
    from google.cloud import storage

    storage_client = storage.Client.from_service_account_json(
        GOOGLE_APPLICATION_CREDENTIALS)
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DF_PROJECT_ID, DF_SESSION_ID)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        logging.debug('Есть ответ на реплику')
        return None, response.query_result.fulfillment_text
    else:
        logging.debug('Нет ответа на реплику')
        return True, response.query_result.fulfillment_text
