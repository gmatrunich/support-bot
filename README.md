# Чат-бот для помощи службе поддержки

Чат-бот для ответов на часто задаваемые вопросы.

Код выполняет три задачи:
1) Отвечает на часто задаваемые вопросы в чат-боте в Телеграме.
2) Отвечает на часто задаваемые вопросы в чат-боте в VK (и не отвечает, если у него нет ответа на вопрос).
3) Бот обучается на готовых данных с помощью DialogFlow.

## Как установить

Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей.
`pip install -r requirements.txt`

Параметры `TELEGRAM_BOT_TOKEN`, `DF_PROJECT_ID`, `DF_PROJECT_NUMBER`, `GOOGLE_APPLICATION_CREDENTIALS`, `VK_BOT_TOKEN` и `TELEGRAM_CHAT_ID` должны находится в файле `.env` рядом со скриптом.

Чтобы получить `TELEGRAM_BOT_TOKEN`, пройдите процесс регистрации нового чат-бота в Telegram: @BotFather

Чтобы получить свой `TELEGRAM_CHAT_ID`, напишите в Telegram специальному боту: @userinfobot

Узнать `DF_PROJECT_ID` и `DF_PROJECT_NUMBER` и получить `GOOGLE_APPLICATION_CREDENTIALS` можно в настройках своего аккаунта DialogFlow.

Для обучения бота у агента DialogFlow должны быть права доступа Администратор Dialogflow API. (В Google Cloud Platform раздел "IAM и администрирование".)

[Гайд по развертыванию ботов на платформе Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

### Как запустить и использовать

1. Для запуска бота в Телеграме используйте команду: `python telegram_bot.py`

2. Для запуска бота в ВК используйте команду `python vk_bot.py`

3. Для обучения бота используйте команду `python df_content.py`. Данные для обучения берутся из файла `questions.json`
[Пример](https://github.com/gmatrunich/support-bot/blob/master/questions.json) JSON-файла с обучающими фразами.

## Пример использования бота

![Sample](https://dvmn.org/media/filer_public/1e/f6/1ef61183-56ad-4094-b3d0-21800bdb8b09/demo_vk_bot.gif)

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/)
