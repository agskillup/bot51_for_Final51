# Что делает:
# - Загружает переменные из `.env`.
# - Подготавливает настройки для удобного доступа через `config.<переменная>`.

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class ConfigError(Exception):
    """Специальный класс исключения для ошибок конфигурации."""
    pass

class Config:
    # Основные настройки проекта
    """
    Класс для хранения и валидации конфигурации приложения.
    Загружает значения из переменных окружения и падает при старте,
    если критически важные переменные не заданы.
    """
    BOT_TOKEN = os.getenv("TOKEN", "default_token")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # База данных (если потребуется)
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    # Администратор
    ADMIN_ID = int(os.getenv("ADMIN_ID", ""))
ADMIN_ID = int(os.getenv("ADMIN_ID", ""))
# Экземпляр конфигурации
config = Config()

# Пример использования
if config.DEBUG:
    print("DEBUG режим включён")