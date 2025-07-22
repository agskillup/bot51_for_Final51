import logging
from pathlib import Path

# Этот код определяет путь к корневой директории проекта.
# Path(__file__) — это путь к текущему файлу (app_logger.py).
# .parent.parent.parent — трижды поднимаемся на уровень выше,
# чтобы добраться от bot/logger/app_logger.py до корня проекта.
ROOT_DIR = Path(__file__).parent.parent.parent

# Создаем полный, абсолютный путь к файлу лога в корневой директории
LOG_FILE_PATH = ROOT_DIR / "bot.log"

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Используем созданный абсолютный путь
        logging.FileHandler(LOG_FILE_PATH, encoding='utf-8'),
        # Также выводим логи в консоль для удобства отладки
        logging.StreamHandler()
    ]
)

# Создаем и экспортируем экземпляр логгера для использования в других модулях
logger = logging.getLogger(__name__)
