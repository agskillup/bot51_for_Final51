# Что делает:
# - Загружает переменные из `.env`.
# - Подготавливает настройки для удобного доступа через `config.<переменная>`.

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    # Основные настройки проекта
    BOT_TOKEN = os.getenv("TOKEN", "default_token")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Настройки API
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    WEATHER_URL = os.getenv("WEATHER_URL", "")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Администратор
    ADMIN_ID = os.getenv("ADMIN_ID", "")

    # База данных (если потребуется)
    DATABASE_URL = os.getenv("DATABASE_URL", "")

# Экземпляр конфигурации
config = Config()

# Пример использования
if config.DEBUG:
    print("DEBUG режим включён")