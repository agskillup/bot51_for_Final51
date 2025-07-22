from bot.base import BotCommand, CommandStrategy
import requests

# # from bot.helper.temperature_helper import Currency1Helper
#
#
# class Currency1Strategy(CommandStrategy):
#     def handle(self, text, chat_id, user_id):
#
#         if text.startswith('/currency1 full'):
#             command = '/currency1 full'
#             text = text.replace('/currency1 full', '')
#         else:
#             command = '/currency1'
#             text = text.replace('/currency1', '')
#
#         url = """https://api.exchangerate.host/list?access_key=b410800238c7ac37f3e4bd1f74bc4799"""
#         response = requests.get(url)
#         data = response.json()
#         return data["success"]
#
# class Currency1Command(BotCommand):
#
#     def __init__(self):
#         self.strategy = Currency1Strategy()
#
#     def execute(self, text, chat_id, user_id):
#         return self.strategy.handle(text, chat_id, user_id)


import re
from bot.base import BotCommand, CommandStrategy
from bot.helper.currency_helper import CurrencyHelper


class Currency1Strategy(CommandStrategy):
    """
    Стратегия для команды /currency1.
    Реализует гибкую конвертацию валют по формату:
    /currency1 <сумма> <ИЗ_ВАЛЮТЫ> to <В_ВАЛЮТУ>
    """

    def __init__(self):
        """
        Инициализирует стратегию и создает экземпляр CurrencyHelper.
        """
        try:
            self.currency_helper = CurrencyHelper()
            self.initialization_error = None
        except ValueError as e:
            self.currency_helper = None
            self.initialization_error = str(e)

    def handle(self, text: str, chat_id: int, user_id: int, **kwargs):
        """
        Обрабатывает команду, парсит аргументы и выполняет конвертацию.
        """
        if not self.currency_helper:
            return f"Ошибка инициализации команды: {self.initialization_error}"

        # Убираем саму команду из текста для удобства парсинга
        clean_text = text.replace('/currency1', '').strip()

        # Используем регулярное выражение для парсинга формата "10 USD to EUR"
        # Оно ищет: (число) (3 буквы) "to" (3 буквы)
        match = re.search(r'(\d+\.?\d*)\s+([A-Z]{3})\s+to\s+([A-Z]{3})', clean_text, re.IGNORECASE)

        if not match:
            return ("Неверный формат команды. Используйте: "
                    "`/currency1 <сумма> <ИЗ_ВАЛЮТЫ> to <В_ВАЛЮТУ>`\n"
                    "Например: `/currency1 10 USD to EUR`")

        # Извлекаем данные из найденных групп
        amount_str, from_currency, to_currency = match.groups()
        amount = float(amount_str)
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Валидируем оба кода валют
        if not self.currency_helper.is_valid_currency(from_currency):
            return f"Неизвестный код исходной валюты: {from_currency}"
        if not self.currency_helper.is_valid_currency(to_currency):
            return f"Неизвестный код целевой валюты: {to_currency}"

        # Выполняем конвертацию через хелпер
        result_data = self.currency_helper.convert(from_currency, to_currency, amount)

        # Обрабатываем результат
        if result_data and result_data.get('success'):
            converted_amount = result_data.get('result')
            if converted_amount is not None:
                return f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
            else:
                return f"Не удалось получить результат конвертации для {from_currency} -> {to_currency}."
        else:
            error_info = result_data.get('error', {}).get('info', 'неизвестная ошибка') if result_data else 'ошибка сети'
            return f"Не удалось выполнить конвертацию. Причина: {error_info}"


class Currency1Command(BotCommand):
    """
    Класс команды /currency1.
    """

    def __init__(self):
        self.strategy = Currency1Strategy()

    def execute(self, text: str, chat_id: int, user_id: int, **kwargs):
        return self.strategy.handle(text, chat_id, user_id)