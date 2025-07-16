# Формируем логику работы с пользователями:

class UserService:
    def __init__(self):
        # Можно подключить базу данных, если такая есть
        self.users = {}

    def add_user(self, user_id: int, name: str) -> None:
        """
        Добавить нового пользователя.
        :param user_id: ID пользователя.
        :param name: Имя пользователя.
        """
        self.users[user_id] = name

    def get_user(self, user_id: int) -> str:
        """
        Получить пользователя по ID.
        :param user_id: ID пользователя.
        :return: Имя пользователя.
        """
        return self.users.get(user_id, "Пользователь не найден")

# Пример использования
if __name__ == "__main__":
    service = UserService()
    service.add_user(1, "John Doe")
    print(service.get_user(1))