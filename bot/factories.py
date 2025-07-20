# Factories.py является центральным "диспетчером" команд

from bot.commands.help_menu import HelpMenuCommand
# from bot.commands.command_dice import DiceCommand
# from bot.commands.command_notebook import NotebookCommand
from bot.commands.command_currency import CurrencyCommand
# from bot.commands.command_iam import IAmCommand
# from bot.commands.command_temperature import TemperatureCommand
# from bot.commands.command_some import SomeCommand
from bot.commands.shutdown import ShutdownCommand
# from bot.commands import COMMAND_CLASSES
from bot.commands.command_dev import DevCommand
# from bot.commands.command_answer import AnswerCommand
from bot.commands.command_currency1 import Currency1Command


# Factory pattern: фабрика для створення команд за ключовим словом
class CommandFactory:
    # commands_map = COMMAND_CLASSES.copy()
    # commands_map["/shutdown"] = ShutdownCommand
    # commands_map["/help"] = HelpMenuCommand

    # Явно определяем все команды в одном месте для ясности и удобства поддержки.
    commands_map = {
        "/help": HelpMenuCommand,
        "/shutdown": ShutdownCommand,
#        "/dice": DiceCommand,
#        "/notebook": NotebookCommand,
        "/currency": CurrencyCommand,
#        "/iam": IAmCommand,
#        "/some": SomeCommand,
        "/dev": DevCommand,
#        "/answer": AnswerCommand,
        "/currency1": Currency1Command,
    }


    @staticmethod
    def create_command(command_name):
        base_command = command_name.split(' ')[0]
        CommandClass = CommandFactory.commands_map.get(base_command)
        if CommandClass:
            return CommandClass()
        return None

# # Преимущества этого подхода:
# 1. Явное объявление: Все команды, включая `/currency` и `/currency1`, явно прописаны в `commands_map`.
# Это гарантирует их работоспособность и упрощает отладку.
# 2. Централизация: Вся логика сопоставления команд находится в одном месте, что соответствует принципу единой ответственности.
# 3. Улучшенная логика: Метод `create_command` теперь корректно обрабатывает команды с параметрами (например, `/notebook add ...`),
# извлекая только базовую часть команды для поиска в словаре.
# 4. Чистота кода: Отсутствует зависимость от внешнего словаря `COMMAND_CLASSES` и лишних импортов, которые не используются напрямую.