import functools
from dotenv import load_dotenv
import os
import logging
from bot.config import config  # Импортируем централизованные настройки
from bot.roles.role_helper import check_command_access


# Настраиваем логгер для этого файла
logger = logging.getLogger(__name__)

class AuthorizationError(Exception):
    """Специальное исключение для ошибок авторизации."""
    pass

# Decorator pattern: логування всіх команд
def log_command(func):
    """Декоратор для логирования вызова команд."""
    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
        # text, chat_id, user_id = args[1:4]
        # print(f"[LOG] Executing command for user {user_id} in chat {chat_id}: {text}")
        # return func(*args, **kwargs)

    def wrapper(self, text: str, chat_id: int, user_id: int, *args, **kwargs):
        # Используем именованные аргументы вместо хрупких индексов
        logger.info(
            f"Команда от user={user_id} в chat={chat_id}: '{text}'"
        )
        return func(self, text, chat_id, user_id, *args, **kwargs)

    return wrapper


# Decorator pattern: перевірка авторизації
def require_auth(func):
    """
    Декоратор для проверки прав доступа пользователя к команде.
    Выбрасывает AuthorizationError в случае отказа в доступе.
    """
    @functools.wraps(func)
    # def wrapper(*args, **kwargs):
    #     load_dotenv()
    #     admin_id = int(os.getenv("ADMIN_ID"))
    #     command = args[1]
    #     user_id = int(args[3])
    #     if user_id == admin_id:
    #         return func(*args, **kwargs)
    #     # Тут відбувається перевірка. Якщо команда не додана в список пускає далі
    #     access = check_command_access(command, user_id)
    #     if access is True:
    #         return func(*args, **kwargs)
    #     else:
    #         return access

    def wrapper(self, text: str, chat_id: int, user_id: int, *args, **kwargs):
        # 4. Получаем ADMIN_ID из настроек, не читая .env каждый раз
        # Предполагаем, что settings.ADMIN_ID уже преобразован в int в конфиге
        if user_id == config.ADMIN_ID:
            return func(self, text, chat_id, user_id, *args, **kwargs)

        # 5. Получаем команду из текста сообщения, а не по индексу
        command = text.split()[0]

        access_result = check_command_access(command, user_id)

        if access_result is True:
            return func(self, text, chat_id, user_id, *args, **kwargs)
        else:
            # 6. Выбрасываем исключение вместо возврата строки
            logger.warning(
                f"Отказ в доступе для user={user_id} к команде '{command}'. Причина: {access_result}"
            )
            raise AuthorizationError(access_result)

    return wrapper
