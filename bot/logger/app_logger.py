# В этом файле можно настроить стандартный модуль `logging` из Python
# для записи логов в файл или вывода в консоль в нужном формате

import logging

# Настраиваем логгер
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Создаем экземпляр логгера для всего приложения
logger = logging.getLogger(__name__)