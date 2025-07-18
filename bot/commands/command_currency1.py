from bot.base import BotCommand, CommandStrategy
import requests
# from bot.helper.temperature_helper import Currency1Helper


class Currency1Strategy(CommandStrategy):
    def handle(self, text, chat_id, user_id):

        if text.startswith('/currency1 full'):
            command = '/currency1 full'
            text = text.replace('/currency1 full', '')
        else:
            command = '/currency1'
            text = text.replace('/currency1', '')

        # # Значення за замовчуванням
        # city = 'Odesa'
        # units = 'metric'

        # if text:
        #     parts = text.split()
        #     if len(parts) >= 1:
        #         city = parts[0]
        #     if len(parts) >= 2:
        #         units = parts[1]

        url = """https://api.exchangerate.host/list?access_key=b410800238c7ac37f3e4bd1f74bc4799"""
        response = requests.get(url)
        data = response.json()
        return data["success"]

#        weather = Currency1Helper(units=units)
#        weather.fetch_weather(city)
#         if command == '/temperature full':
#             result = f"{city}: {weather.get_weather()}"
#         else:
#             result = f"{city}: {weather.get_temperature()}"
#         return result

# class CurrencyService:
#     def __init__(self, api_url: str):
#         self.api_url = api_url
#
#     def get_exchange_rate(self, base: str, target: str) -> float:
#         """
#         Получить курс обмена валют.
#         :param base: Базовая валюта.
#         :param target: Валюта для перевода.
#         :return: Курс обмена.
#         """
#         response = requests.get(f"{self.api_url}?base={base}&symbols={target}")
#         if response.status_code != 200:
#             raise Exception("Ошибка при получении курсов валют")
#         data = response.json()
#         return data["rates"].get(target, 0.0)

# Пример использования
# if __name__ == "__main__":
#     service = CurrencyService("https://api.exchangerate.host/latest")
#     token = "b410800238c7ac37f3e4bd1f74bc4799"
#     print(service.get_exchange_rate("USD", "EUR"))

class Currency1Command(BotCommand):
    info = "Check the current temperature in a city (usage: <city> <units>)"

    def __init__(self):
        self.strategy = Currency1Strategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
