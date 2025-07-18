from bot.commands.help_menu import HelpMenuCommand
from bot.commands.command_dice import DiceCommand
from bot.commands.command_notebook import NotebookCommand
from bot.commands.command_currency import CurrencyCommand
from bot.commands.command_iam import IAmCommand
from bot.commands.command_temperature import TemperatureCommand
from bot.commands.command_some import SomeCommand
from bot.commands.shutdown import ShutdownCommand
from bot.commands import COMMAND_CLASSES
from bot.commands.command_dev import DevCommand
from bot.commands.command_answer import AnswerCommand
from bot.commands.command_currency1 import Currency1Command




# Factory pattern: фабрика для створення команд за ключовим словом
class CommandFactory:
    commands_map = COMMAND_CLASSES.copy()
    commands_map["/shutdown"] = ShutdownCommand
    commands_map["/help"] = HelpMenuCommand

    @staticmethod
    def create_command(command_name):
        CommandClass = CommandFactory.commands_map.get(command_name)
        if CommandClass:
            return CommandClass()
        return None
