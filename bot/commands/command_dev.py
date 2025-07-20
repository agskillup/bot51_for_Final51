from bot.base import BotCommand, CommandStrategy
import os

# При вызове команды `/dev` в чате, бот выполняет код из `DevStrategy` и
# возвращает строку, содержащую уникальный идентификатор пользователя в
# Telegram (`user_id`) и идентификатор чата (`chat_id`), из которого
# была вызвана команда.
# Текущий результат выполнения команды: `Dev ID: {user_id}, chat: {chat_id}`
# Это базовый, но очень полезный инструмент для разработчика,
# чтобы проверить, правильно ли бот идентифицирует пользователя и чат, из которого пришло сообщение.

# class DevStrategy(CommandStrategy):
#     def handle(self, text, chat_id, user_id):
#         # Корисне навантаження
#         return f"Dev ID: {user_id}, chat: {chat_id}"

# Добавлена структура для обработки подкоманд, а также "заглушка" для проверки
# прав администратора (является хорошей практикой для подобных инструментов)
class DevStrategy(CommandStrategy):
    def __init__(self):
        # Загружаем ID администраторов из переменных окружения (указано в .env файле)
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        self.admin_ids = [int(admin_id) for admin_id in admin_ids_str.split(',') if admin_id.isdigit()]

        # Словарь для сопоставления подкоманд с методами-обработчиками
        self.dev_commands = {
            "get_ids": self._get_ids,
            "help": self._show_help,    # <--- Вот здесь мы связываем подкоманду "help"
        }

    def handle(self, text, chat_id, user_id):
        # проверка администратора включена и работает с .env
        if user_id not in self.admin_ids:
            return "⛔ У вас нет доступа к этой команде."

        # Разбиваем текст команды на части, чтобы отделить команду от аргументов
        parts = text.split()
#        sub_command = parts[1] if len(parts) > 1 else None
        # parts[0] это /dev, parts[1] может быть подкомандой
        sub_command = parts[1] if len(parts) > 1 else "get_ids"
        args = parts[2:] if len(parts) > 2 else []

        # Выбираем нужный метод из словаря или метод по умолчанию
        handler = self.dev_commands.get(sub_command, self._unknown_command)

        # # Вызываем обработчик, передавая ему аргументы
        # return handler(chat_id=chat_id, user_id=user_id, args=args)

        try:
            # Безопасно вызываем обработчик
            return handler(chat_id=chat_id, user_id=user_id, args=args)
        except Exception as e:
            # В случае ошибки в подкоманде, возвращаем информативное сообщение
            return f"❌ Произошла ошибка при выполнении команды `{sub_command}`: {e}"

    # --- Приватные методы для каждой подкоманды ---
    # оставляем как _get_ids и _unknown_command как обычный метод экземпляра, так как
    # главная причина - Архитектурное единообразие:
    # 1. у нас есть словарь `self.dev_commands`, который сопоставляет строковые команды с методами-обработчиками;
    # 2. Основной метод `handle` получает нужный обработчик из этого словаря и вызывает его, передавая стандартный набор аргументов: `handler(chat_id=..., user_id=..., args=...)`.
    # Метод `_show_help` и нуждается в `self`, чтобы получить доступ к `self.dev_commands`.
    # Если мы сделаем _get_ids и _unknown_command статическими, а `_show_help` оставим обычным методом, мы создадим неоднородную систему: в словаре будут храниться обработчики разных типов.
    # Технически это будет работать, но это усложнит понимание и поддержку кода.
    # Сохраняя все обработчики как методы экземпляра, мы придерживаемся простого и понятного правила:
    # "Каждая подкоманда в **`DevStrategy`** реализуется как метод этого же класса с одинаковой сигнатурой".

    # Краткий вывод: Сохранение _get_ids и _unknown_command как методов экземпляра поддерживает единообразие, читаемость и целостность класса DevStrategy.
    # Неиспользуемый `self` - это крошечная и приемлемая плата за эти архитектурные преимущества.
    # Поэтому изменять их не нужно.

    def _get_ids(self, chat_id, user_id, args):
        """Возвращает ID пользователя и чата. Работает по умолчанию."""
        return f"🆔 **User ID:** `{user_id}`\n**Chat ID:** `{chat_id}`"

    def _show_help(self, **kwargs):
        """Показывает список доступных dev-команд."""
        available_commands = "\n".join(f"- `{cmd}`" for cmd in self.dev_commands.keys())
        return f"🛠️ **Доступные команды разработчика:**\n{available_commands}"

    def _unknown_command(self, **kwargs):
        """Вызывается, если подкоманда не найдена."""
        return f"❓ Неизвестная подкоманда. Используйте `/dev help` для справки."

class DevCommand(BotCommand):
    def __init__(self):
        self.strategy = DevStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
