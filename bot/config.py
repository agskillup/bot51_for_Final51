# Что делает:
# - Загружает переменные из `.env`.
# - Подготавливает настройки для удобного доступа через `config.<переменная>`.

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Администратор
ADMIN_ID = os.getenv("ADMIN_ID", "")

class Config:
    # Основные настройки проекта
    BOT_TOKEN = os.getenv("TOKEN", "default_token")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # База данных (если потребуется)
    DATABASE_URL = os.getenv("DATABASE_URL", "")

# Экземпляр конфигурации
config = Config()

# Пример использования
if config.DEBUG:
    print("DEBUG режим включён")