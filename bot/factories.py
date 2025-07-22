# Factories.py является центральным "диспетчером" команд

from typing import Optional, Dict
from bot.base import BotCommand  # Импортируем базовый класс для type hinting
from bot.commands.help_menu import HelpMenuCommand
from bot.commands.command_currency import CurrencyCommand
from bot.commands.shutdown import ShutdownCommand
from bot.commands.command_dev import DevCommand
from bot.commands.command_currency1 import Currency1Command


# Factory pattern: фабрика для створення команд за ключовим словом
class CommandFactory:
    """
    Фабрика для управления экземплярами команд.
    Использует словарь для хранения единственного экземпляра каждой команды (Singleton-like),
    чтобы избежать их пересоздания при каждом вызове.
    """
    # Явно определяем все команды в одном месте для ясности и удобства поддержки.
    command_map: Dict[str, type[BotCommand]] = {
        "/help": HelpMenuCommand,
        "/shutdown": ShutdownCommand,
        "/currency": CurrencyCommand,
        "/dev": DevCommand,
        "/currency1": Currency1Command,
    }

    # 2. Словарь для хранения ЕДИНСТВЕННЫХ экземпляров команд.
    # Он будет лениво заполняться при первом запросе команды.
    command_instances: Dict[str, BotCommand] = {}

    @staticmethod
    # def create_command(command_name):
    def create_command(command_name: str) -> Optional[BotCommand]:
        """
        Возвращает экземпляр команды по ее имени.
        Если экземпляр для этой команды еще не создан, он будет создан
        и сохранен для последующего переиспользования.
        """
        base_command = command_name.split(' ')[0]
        # CommandClass = CommandFactory.commands_map.get(base_command)
        # if CommandClass:
        #     return CommandClass()

        # Проверяем, есть ли у нас уже готовый экземпляр.
        if base_command in CommandFactory.command_instances:
            return CommandFactory.command_instances[base_command]

        # 4. Если экземпляра нет, ищем класс команды.
        CommandClass = CommandFactory.command_map.get(base_command)
        if CommandClass:
            # 5. Создаем экземпляр ОДИН РАЗ и сохраняем его.
            instance = CommandClass()
            CommandFactory.command_instances[base_command] = instance
            return instance

        return None

    @staticmethod
    def get_available_commands() -> dict[str, BotCommand]:
        """
        Возвращает словарь всех доступных КЛАССОВ команд для использования, например, в /help.
        Это позволяет команде /help самой решать, как отображать информацию (например, из docstring класса).
        """
        return CommandFactory.command_instances

# # Преимущества этого подхода:
# 1. Явное объявление: Все команды, включая `/currency` и `/currency1`, явно прописаны в `commands_map`.
# Это гарантирует их работоспособность и упрощает отладку.
# 2. Централизация: Вся логика сопоставления команд находится в одном месте, что соответствует принципу единой ответственности.
# 3. Улучшенная логика: Метод `create_command` теперь корректно обрабатывает команды с параметрами (например, `/notebook add ...`),
# извлекая только базовую часть команды для поиска в словаре.
# 4. Чистота кода: Отсутствует зависимость от внешнего словаря `COMMAND_CLASSES` и лишних импортов, которые не используются напрямую.