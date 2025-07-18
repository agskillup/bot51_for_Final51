import os
import requests
import time
from bot.factories import CommandFactory
from bot.decorators import log_command, require_auth
from bot.handlers import Handler, CensorshipHandler, LoggingHandler


# Singleton pattern: тільки один екземпляр TelegramBot
class TelegramBot:
    _instance = None

    def __new__(cls, token):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{self.token}/"
        self.handler_chain = self.build_handler_chain()

    def build_handler_chain(self):
        # Chain of Responsibility: censorship -> logging -> команда
        censorship = CensorshipHandler()
        logging = LoggingHandler()
        censorship.set_next(logging)
        return censorship

    @log_command
    @require_auth
    def handle_message(self, text, chat_id, user_id):
        # Chain of Responsibility: запускаємо ланцюг
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

                # self.send_message(chat_id, reply)
                self.last_update_id = update["update_id"]
