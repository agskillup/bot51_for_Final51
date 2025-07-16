# Что делает:
# - Создаёт логгер с ротацией файлов (`bot.log`).
# - Подключает форматирование и уровни логов.
# - Можно импортировать `logger` и использовать в любом модуле проекта.

import logging
from logging.handlers import RotatingFileHandler

# Настройка форматирования
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Общая конфигурация
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (по умолчанию DEBUG)
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)

# Ротация логов с сохранением 5 файлов по 1MB
file_handler = RotatingFileHandler(
    "bot.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Добавляем обработчик в главный логгер
logger = logging.getLogger("bot")
logger.addHandler(file_handler)

# Пример использования
logger.info("Логгер успешно настроен")