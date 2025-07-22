# Исправляем нарушение Принципа подстановки Барбары Лисков (Liskov Substitution Principle).
# Простыми словами: дочерний класс не должен изменять данные родительского класса

from abc import ABC, abstractmethod
from typing import Optional


# Command pattern: Абстрактний клас для всіх команд
class BotCommand(ABC):
    @abstractmethod
    # def execute(self, text, chat_id, user_id):

    # добавлен атрибут `kwargs`, чтоб сделать класс более гибкой (- в файле унаследованный класс переопределяет его уже с другой сигнатурой: `execute(self, text, chat_id, user_id, **kwargs)` `role.py``RoleCommand`)
    def execute(self, text: str, chat_id: int, user_id: int, **kwargs) -> Optional[str]:
        pass

# Strategy pattern: Базовий клас для різних стратегій поведінки
class CommandStrategy(ABC):
    @abstractmethod
    # def handle(self, text, chat_id, user_id):
    def handle(self, text: str, chat_id: int, user_id: int, **kwargs) -> Optional[str]:
        pass
