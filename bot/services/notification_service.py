# модуля для отправки уведомлений:

# class NotificationService:
#     def send_message(self, user_id: int, message: str) -> None:
#         """
#         Отправить сообщение пользователю (заглушка).
#         :param user_id: ID пользователя.
#         :param message: Текст сообщения.
#         """
#         print(f"Отправка сообщения пользователю {user_id}: {message}")
#
# # Пример использования
# if __name__ == "__main__":
#     service = NotificationService()
#     service.send_message(1, "Привет! Это пример уведомления.")


import logging
from bot.core import TelegramBot
from bot.services.user_service import UserService

# Настраиваем логирование для этого файла
logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, bot: TelegramBot, user_service: UserService):
        """
        Инициализирует сервис уведомлений.
        Для работы сервис должен получить готовые экземпляры бота и сервиса пользователей.

        :param bot: Экземпляр TelegramBot для фактической отправки сообщений.
        :param user_service: Сервис для работы с пользователями (чтобы знать, кому отправлять).
        """
        self.bot = bot
        self.user_service = user_service

    def send_message_to_user(self, user_id: int, message: str) -> None:
        """
        Отправляет личное сообщение конкретному пользователю.
        В Telegram API для личного сообщения chat_id совпадает с user_id.

        :param user_id: ID пользователя Telegram.
        :param message: Текст сообщения для отправки.
        """
        try:
            # Используем метод send_message из уже существующего объекта бота
            self.bot.send_message(chat_id=user_id, text=message)
            logger.info(f"Уведомление для пользователя {user_id} успешно отправлено.")
        except Exception as e:
            # Логируем возможные ошибки (например, если бот заблокирован пользователем)
            logger.error(f"Не удалось отправить уведомление пользователю {user_id}: {e}")

    def broadcast_to_all_users(self, message: str) -> None:
        """
        Выполняет рассылку сообщения всем пользователям, которые есть в базе данных.
        """
        all_user_ids = self.user_service.get_all_user_ids()

        if not all_user_ids:
            logger.warning("Рассылка отменена: в базе данных нет ни одного пользователя.")
            return

        logger.info(f"Начало рассылки сообщения для {len(all_user_ids)} пользователей.")

        successful_sends = 0
        for user_id in all_user_ids:
            try:
                self.send_message_to_user(user_id, message)
                successful_sends += 1
            except Exception as e:
                # Ошибка с одним пользователем не должна прерывать всю рассылку
                logger.error(f"Ошибка при рассылке пользователю {user_id}: {e}")

        logger.info(f"Рассылка завершена. Успешно отправлено {successful_sends} из {len(all_user_ids)} сообщений.")
