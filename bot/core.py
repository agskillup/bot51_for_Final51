import os
import sys
import requests
import time
from typing import Optional, Any, Dict
from bot.factories import CommandFactory
from bot.decorators import log_command, require_auth
from bot.handlers import CensorshipHandler, LoggingHandler
from bot.logger.app_logger import logger


# Singleton pattern: тільки один екземпляр TelegramBot
class TelegramBot:
    """
    Основной класс бота, реализующий long-polling и обработку сообщений.
    Реализован как Singleton для гарантии единственного экземпляра.
    """
#    _instance = None
    _instance: Optional['TelegramBot'] = None
    # Константа для команды выключения, чтобы избежать "магических строк"
    SHUTDOWN_COMMAND_REPLY = "__SHUTDOWN__"

#    def __new__(cls, token):
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

#    def __init__(self, token):
    def __init__(self, token: str):
        # Предотвращаем повторную инициализацию
        if hasattr(self, 'is_initialized'):
            return

        self.token: str = token
        self.url = f"https://api.telegram.org/bot{self.token}/"
        self.last_update_id: Optional[int] = None
        self.handler_chain = self.build_handler_chain()
        self.is_initialized: bool = True
        logger.info("Экземпляр TelegramBot инициализирован.")

#    def build_handler_chain(self):
    def build_handler_chain(self) -> CensorshipHandler:
        """Собирает и возвращает цепочку обработчиков."""
        # Chain of Responsibility: censorship -> logging -> команда
        censorship = CensorshipHandler()
        logging = LoggingHandler()
        censorship.set_next(logging)
        return censorship

    @log_command
    @require_auth
    # def handle_message(self, text, chat_id, user_id):
    #     # Chain of Responsibility: запускаємо ланцюг
    def handle_message(self, text: str, chat_id: int, user_id: int) -> Optional[str]:
        """
        Обрабатывает входящее текстовое сообщение, прогоняя его через
        цепочку обязанностей и фабрику команд.
        """
        # 1. Цепочка обязанностей (цензура, логирование)
        result = self.handler_chain.handle(text, chat_id, user_id)
        if result:
            return result
        # Factory pattern: створюємо команду
        command_name = text.split()[0]
        command = CommandFactory.create_command(command_name)
        if command:
            return command.execute(text, chat_id, user_id)
        return "Unknown command. Type /help."

    def get_last_update(self):
        url = self.url + "getUpdates?timeout=10"
        response = requests.get(url)
        result = response.json()["result"]
        if result:
            return result[-1]
        return None

    def get_chat_id(self, update):
        return update["message"]["chat"]["id"]

    def get_user_id(self, update):
        return update["message"]["from"]["id"]

    def get_message_text(self, update):
        return update["message"]["text"]

    def send_message(self, chat_id, text):
        url = self.url + "sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)

    def run(self):
        update = self.get_last_update()
        if update:
            self.last_update_id = update['update_id']
        else:
            self.last_update_id = None
        while True:
            time.sleep(1.5)
            update = self.get_last_update()
            if update and update["update_id"] != self.last_update_id:
                # Проверяем, есть ли в обновлении текстовое сообщение
                if "message" in update and "text" in update["message"]:

                    chat_id = self.get_chat_id(update)
                    user_id = self.get_user_id(update)
                    message_text = self.get_message_text(update)
                    reply = self.handle_message(message_text, chat_id, user_id)
                    if reply == "__SHUTDOWN__":
                        self.send_message(chat_id, "Бот вимикається…")
                        import sys
                        sys.exit(0)
                    else:
                        self.send_message(chat_id, reply)

                # ВАЖНО: обновляем ID последнего обновления в любом случае,
                # чтобы не зацикливаться на обработке нетекстовых сообщений.
                self.last_update_id = update["update_id"]
