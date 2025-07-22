# Формируем логику работы с пользователями:

# class UserService:
#     def __init__(self):
#         # Можно подключить базу данных, если такая есть
#         self.users = {}
#
#     def add_user(self, user_id: int, name: str) -> None:
#         """
#         Добавить нового пользователя.
#         :param user_id: ID пользователя.
#         :param name: Имя пользователя.
#         """
#         self.users[user_id] = name
#
#     def get_user(self, user_id: int) -> str:
#         """
#         Получить пользователя по ID.
#         :param user_id: ID пользователя.
#         :return: Имя пользователя.
#         """
#         return self.users.get(user_id, "Пользователь не найден")

import sqlite3
import logging

# Получаем логгер для вывода информации
logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db_path='users.db'):
        """
        Инициализирует сервис, подключается к базе данных и создает таблицу,
        если она не существует.

        :param db_path: Путь к файлу базы данных SQLite.
        """
        self.db_path = db_path
        self._create_table_if_not_exists()

    def _get_connection(self):
        """Создает и возвращает соединение с базой данных."""
        return sqlite3.connect(self.db_path)

    def _create_table_if_not_exists(self):
        """
        Создает таблицу 'users' для хранения данных о пользователях,
        если она еще не была создана.
        """
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("""
                     CREATE TABLE IF NOT EXISTS users (
                         user_id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )
                """)
            logger.info(f"Таблица 'users' в базе данных '{self.db_path}' готова к работе.")
        except sqlite3.Error as e:
            logger.error(f"Ошибка при создании таблицы 'users': {e}")
        finally:
            conn.close()

    def add_user(self, user_id: int, name: str) -> None:
        """
        Добавляет нового пользователя или обновляет имя существующего.
        Использует 'INSERT OR REPLACE' для атомарной операции.

        :param user_id: ID пользователя.
        :param name: Имя пользователя.
        """
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    "INSERT OR REPLACE INTO users (user_id, name) VALUES (?, ?)",
                    (user_id, name)
                )
            logger.info(f"Пользователь {user_id} ({name}) был добавлен или обновлен.")
        except sqlite3.Error as e:
            logger.error(f"Ошибка при добавлении пользователя {user_id}: {e}")
        finally:
            conn.close()

    def get_user(self, user_id: int) -> str:
        """
        Получает имя пользователя по ID из базы данных.

        :param user_id: ID пользователя.
        :return: Имя пользователя или стандартное сообщение, если он не найден.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()  # Получаем одну запись

            if result:
                return result[0]  # Возвращаем имя пользователя (первый столбец)
            else:
                return "Пользователь не найден"
        except sqlite3.Error as e:
            logger.error(f"Ошибка при поиске пользователя {user_id}: {e}")
            return "Ошибка при доступе к базе данных"
        finally:
            conn.close()


# Пример использования
if __name__ == "__main__":
    service = UserService()
    service.add_user(1, "John Doe")
    print(service.get_user(1))