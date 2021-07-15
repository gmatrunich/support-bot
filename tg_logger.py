import logging


class TGLogsHandler(logging.Handler):

    def __init__(self, telegram_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.telegram_bot = telegram_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(chat_id=self.chat_id, text=log_entry)
