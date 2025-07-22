import requests
from bot.base import BotCommand, CommandStrategy

# class CurrencyStrategy(CommandStrategy):
#     def fetch_rate(self, valcode='USD'):
#         """Отримати курс valcode до гривні через API НБУ"""
#         try:
#             url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={valcode}&json"
#             resp = requests.get(url, timeout=5)
#             resp.raise_for_status()
#             data = resp.json()
#             if data and isinstance(data, list) and "rate" in data[0]:
#                 rate = data[0]["rate"]
#                 return rate
#             return None
#         except Exception as e:
#             return None
#
#     def handle(self, text, chat_id, user_id):
#         # /currency USD  або просто /currency
#         valcode = 'USD'
#         if text.strip().upper().startswith('/CURRENCY'):
#             parts = text.strip().split()
#             if len(parts) > 1:
#                 valcode = parts[1].upper()
#         rate = self.fetch_rate(valcode)
#         if rate:
#             return f"1 {valcode} = {rate:.2f} UAH (НБУ)"
#         else:
#             return f"Не вдалося отримати курс для {valcode}"
#
# class CurrencyCommand(BotCommand):
#     def __init__(self):
#         self.strategy = CurrencyStrategy()
#
#     def execute(self, text, chat_id, user_id):
#         return self.strategy.handle(text, chat_id, user_id)


# Импортируем базовые классы из центрального файла bot/base.py
from bot.base import BotCommand, CommandStrategy
from bot.helper.currency_helper import CurrencyHelper


class CurrencyStrategy(CommandStrategy):
    """
    Стратегия для команды /currency.
    Использует CurrencyHelper для получения курса указанной валюты к UAH.
    """

    def __init__(self):
        """
        Инициализирует стратегию и создает экземпляр CurrencyHelper.
        """
        try:
            self.currency_helper = CurrencyHelper()
        except ValueError as e:
            # Если хелпер не смог создаться (например, нет .env переменных),
            # он будет None, и команда вернет ошибку.
            self.currency_helper = None
            self.initialization_error = str(e)

    def handle(self, text: str, chat_id: int, user_id: int, **kwargs):
        """
        Обрабатывает команду. Формат: /currency [КОД_ВАЛЮТЫ].
        По умолчанию используется USD.
        """
        if not self.currency_helper:
            return f"Ошибка инициализации команды: {self.initialization_error}"

        # Определяем код валюты из текста команды
        parts = text.strip().split()
        valcode = 'USD'  # Валюта по умолчанию
        if len(parts) > 1:
            valcode = parts[1].upper()

        # Шаг 1: Валидация валюты через хелпер
        if not self.currency_helper.is_valid_currency(valcode):
            return (f"Не удалось найти валюту с кодом '{valcode}'. "
                    f"Пожалуйста, используйте стандартный трехбуквенный код (например, USD, EUR).")

        # Шаг 2: Выполняем конвертацию через хелпер (к UAH)
        result_data = self.currency_helper.convert(from_currency=valcode, to_currency='UAH', amount=1.0)

        # Шаг 3: Обрабатываем результат
        if result_data and result_data.get('success'):
            rate = result_data.get('result')
            if rate is not None:
                return f"1 {valcode} = {rate:.2f} UAH"
            else:
                return f"Не удалось получить результат конвертации для {valcode}."
        else:
            error_info = result_data.get('error', {}).get('info', 'неизвестная ошибка') if result_data else 'ошибка сети'
            return f"Не удалось получить курс для {valcode}. Причина: {error_info}"


class CurrencyCommand(BotCommand):
    """
    Класс команды /currency.
    Эта структура полностью соответствует другим командам в проекте.
    """

    def __init__(self):
        """
        При создании команды, инициализируем ее стратегию.
        """
        self.strategy = CurrencyStrategy()

    def execute(self, text: str, chat_id: int, user_id: int, **kwargs):
        """
        Выполняет команду, вызывая обработчик из стратегии.
        Этот метод вызывается из фабрики команд.
        """
        return self.strategy.handle(text, chat_id, user_id)