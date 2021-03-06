import tg_logger
import df_api
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import telegram
import logging
import os


logger = logging.getLogger('telegram_logger')


if __name__ == "__main__":
    telegram_bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
    logger.setLevel(logging.WARNING)
    logger.addHandler(tg_logger.TGLogsHandler(
        telegram_bot,
        os.environ['TELEGRAM_CHAT_ID'])
    )

    vk_session = vk_api.VkApi(token=os.environ['VK_BOT_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            has_answer, bot_answer = df_api.detect_intent_text(event.text)
            if has_answer:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=bot_answer,
                    random_id=random.randint(1, 1000)
                )
