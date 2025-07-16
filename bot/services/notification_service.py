# модуля для отправки уведомлений:

class NotificationService:
    def send_message(self, user_id: int, message: str) -> None:
        """
        Отправить сообщение пользователю (заглушка).
        :param user_id: ID пользователя.
        :param message: Текст сообщения.
        """
        print(f"Отправка сообщения пользователю {user_id}: {message}")

# Пример использования
if __name__ == "__main__":
    service = NotificationService()
    service.send_message(1, "Привет! Это пример уведомления.")