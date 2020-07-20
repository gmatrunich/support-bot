import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import dialogflow_v2 as dialogflow
import os
from dotenv import load_dotenv


load_dotenv()
VK_BOT_TOKEN = os.environ['VK_BOT_TOKEN']
DF_PROJECT_ID = os.environ['DF_PROJECT_ID']
DF_PROJECT_NUMBER = os.environ['DF_PROJECT_NUMBER']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
DF_SESSION_ID = os.environ['DF_SESSION_ID']
LANGUAGE_CODE = 'ru'


def echo(bot_answer, event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=bot_answer,
        random_id=random.randint(1, 1000)
    )


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

    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            bot_answer = detect_intent_text(
                DF_PROJECT_ID, DF_SESSION_ID, event.text, LANGUAGE_CODE
                )
            if bot_answer is not None:
                echo(bot_answer, event, vk_api)
