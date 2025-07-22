# import os
# import importlib
# import inspect
# from bot.base import BotCommand, CommandStrategy
# Импортируем базовый класс, чтобы можно было достать описание
from typing import Optional

from bot.base import BotCommand, CommandStrategy


class HelpMenuStrategy(CommandStrategy):
    def handle(self, text: str, chat_id: int, user_id: int, **kwargs) -> Optional[str]:
        # Импортируем нашу фабрику сюда.
        # Причина: 'factories.py' импортирует `HelpMenuCommand` из `help_menu.py`
        # и `help_menu.py` импортирует `CommandFactory` из `factories.py` одновременно,
        # что в итоге порождает циклическую ошибку в `main.py`
        # Таким образом разрываем цепочку и устраняем циклическую ошибку.
        from bot.factories import CommandFactory
        help_text = "Здравствуйте! Я бот. Доступные команды:\n"

        # Получаем словарь { 'имя_команды': КлассКоманды } из фабрики
        commands_map = CommandFactory.command_map

        # Сортируем команды по имени для красивого вывода
        for command_name in sorted(commands_map.keys()):
            # Получаем класс команды, например, DevCommand
            CommandClass = commands_map[command_name]

            # Используем docstring класса как описание. Это стандартный подход в Python.
            # Если docstring нет, используем запасной текст.
            description = CommandClass.__doc__ or "Описание отсутствует."

            # Убираем лишние пробелы из многострочных docstrings
            description = " ".join(description.strip().split())

            help_text += f"{command_name} - {description}\n"

        return help_text


# class HelpMenuStrategy(CommandStrategy):
#     def handle(self, text, chat_id, user_id):
#         # Генеруємо команди прямо тут
#         commands_dir = os.path.dirname(__file__)
#         command_infos = {}
#         for file in os.listdir(commands_dir):
#             if file.startswith("command_") and file.endswith(".py"):
#                 module_name = f"bot.commands.{file[:-3]}"
#                 module = importlib.import_module(module_name)
#                 for name, obj in inspect.getmembers(module):
#                     if inspect.isclass(obj) and issubclass(obj, BotCommand) and obj is not BotCommand:
#                         info = getattr(obj, "info", "No description")
#                         command_infos[f"/{file[8:-3]}"] = info
#                         break
#         command_infos["/help"] = "Show this help menu"
#
#         help_text = "This is help menu. Available commands:\n"
#         for cmd, info in sorted(command_infos.items()):
#             help_text += f"{cmd} - {info}\n"
#
#         return help_text


class HelpMenuCommand(BotCommand):
    def __init__(self):
        self.strategy = HelpMenuStrategy()

    def execute(self, text: str, chat_id: int, user_id: int, **kwargs) -> Optional[str]:
        return self.strategy.handle(text, chat_id, user_id)
