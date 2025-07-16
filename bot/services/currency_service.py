# Файл, который реализует работу с курсами валют

import requests

class CurrencyService:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_exchange_rate(self, base: str, target: str) -> float:
        """
        Получить курс обмена валют.
        :param base: Базовая валюта.
        :param target: Валюта для перевода.
        :return: Курс обмена.
        """
        response = requests.get(f"{self.api_url}?base={base}&symbols={target}")
        if response.status_code != 200:
            raise Exception("Ошибка при получении курсов валют")
        data = response.json()
        return data["rates"].get(target, 0.0)

# Пример использования
if __name__ == "__main__":
    service = CurrencyService("https://api.exchangerate.host/latest")
    print(service.get_exchange_rate("USD", "EUR"))