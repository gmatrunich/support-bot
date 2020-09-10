from base import *
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import telegram
import logging
import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
VK_BOT_TOKEN = os.environ['VK_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']


logger = logging.getLogger('telegram_logger')


def echo(bot_answer, event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=bot_answer,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    telegram_bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(telegram_bot, TELEGRAM_CHAT_ID))

    vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    try:
        longpoll = VkLongPoll(vk_session)
    except Exception as err:
        logger.exception(err)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            has_answer, bot_answer = detect_intent_text(event.text)
            if has_answer is not None:
                try:
                    echo(bot_answer, event, vk_api)
                except requests.exceptions.HTTPError as err:
                    logger.warning(f'Something has gone wrong!\n{err}')
