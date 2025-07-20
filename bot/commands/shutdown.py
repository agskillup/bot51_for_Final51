# обеспечивает безопасное и контролируемое завершение работы

from bot.base import BotCommand, CommandStrategy

class ShutdownStrategy(CommandStrategy):
    def handle(self, text, chat_id, user_id):
        # Можна тут повертати спец. маркер
        return "__SHUTDOWN__"

class ShutdownCommand(BotCommand):
    """(Только для администратора) Безопасно завершает работу бота."""
    def __init__(self):
        self.strategy = ShutdownStrategy()

    # если обычный пользователь попробует выполнить команду `/shutdown`,
    # он получит вежливый отказ, а бот продолжит работать.
    # Сигнал `__SHUTDOWN__` будет отправлен только в том случае,
    # если команду вызовет администратор
    def execute(self, text, chat_id, user_id):
        # Импортируем ID администратора из конфига сюда, чтоб исключить циклическую ошибку
        from bot.config import ADMIN_ID
        # Добавляем проверку прав доступа
        # Сравниваем ID пользователя с ID администратора
        if str(user_id) != str(ADMIN_ID):
            # Если ID не совпадают, возвращаем сообщение об ошибке
            # и прекращаем выполнение команды.
            return "У вас нет прав для выполнения этой команды."

        # Если проверка пройдена, выполняем основную логику
        return self.strategy.handle(text, chat_id, user_id)
