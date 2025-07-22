# Исправляем нарушение Принципа подстановки Барбары Лисков (Liskov Substitution Principle).
# Простыми словами: дочерний класс не должен изменять данные родительского класса

from abc import ABC, abstractmethod
from typing import Optional


# Command pattern: Абстрактний клас для всіх команд
class BotCommand(ABC):
    """
    Абстрактный базовый класс для всех команд бота.
    Определяет единый интерфейс для выполнения команд.
    """
    @abstractmethod
    # def execute(self, text, chat_id, user_id):

    # добавлен атрибут `kwargs`, чтоб сделать класс более гибкой (- в файле унаследованный класс переопределяет его уже с другой сигнатурой: `execute(self, text, chat_id, user_id, **kwargs)` `role.py``RoleCommand`)
    def execute(self, text: str, chat_id: int, user_id: int, **kwargs) -> Optional[str]:
        """
        Основной метод, который выполняет логику команды.
        Этот метод должен быть реализован во всех дочерних классах.

        :param text: Полный текст сообщения от пользователя.
        :param chat_id: ID чата, из которого пришла команда.
        :param user_id: ID пользователя, отправившего команду.
        :param kwargs: Дополнительные именованные аргументы для гибкости.
        :return: Строка с ответом для пользователя или None, если ответ не требуется.
        """
        pass

# Strategy pattern: Базовий клас для різних стратегій поведінки
class CommandStrategy(ABC):
    """
    Абстрактный базовый класс для различных стратегий, которые могут
    использоваться внутри одной или нескольких команд.
    """
    @abstractmethod
    # def handle(self, text, chat_id, user_id):
    def handle(self, text: str, chat_id: int, user_id: int, **kwargs) -> Optional[str]:
        """
        Основной метод, который выполняет логику конкретной стратегии.

        :param text: Полный текст сообщения от пользователя.
        :param chat_id: ID чата.
        :param user_id: ID пользователя.
        :param kwargs: Дополнительные именованные аргументы.
        :return: Строка с результатом выполнения или None.
        """
        pass
