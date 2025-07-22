# ### Ключевые изменения и преимущества:
# Этот класс играет важную роль в архитектуре проекта,
# следуя принципу единой ответственности (Single Responsibility Principle).
# Он изолирует всю логику работы с API курсов валют в одном месте.
# Это делает остальной код (например, команды бота или стратегии) более чистым и простым,
# поскольку им не нужно знать детали реализации взаимодействия с API.

# 1. Корректная логика: Класс теперь полностью сфокусирован на работе с валютами.
# 2. Работа с API: Методы `convert` и `_make_request` предназначены для выполнения реальных запросов к API курсов валют.
# 3. Конфигурация через `.env`: Ключ и базовый URL для API загружаются из переменных окружения (`CURRENCY_API_KEY`, `CURRENCY_API_URL`), что является безопасной практикой.
# 4. Валидация валют: Метод `is_valid_currency` позволяет быстро проверить, корректный ли код валюты ввел пользователь, используя данные из `currency.json`.
# 5. Кеширование: Класс использует `currency.json` как кеш. Если файл пуст или отсутствует, метод `update_currencies_cache` может запросить свежий список валют из API и сохранить его. Это снижает количество ненужных запросов.
# 6. Надежность: Код включает обработку ошибок сети и HTTP, возвращая `None` в случае неудачи, что позволяет вызывающему коду адекватно реагировать на сбои.

from locale import currency

import os
import requests
from dotenv import load_dotenv
import json
from pathlib import Path


class CurrencyHelper:
    """
    Вспомогательный класс для работы с API курсов валют.
    Осуществляет запросы к API, обрабатывает ответы и предоставляет
    методы для получения информации о курсах и доступных валютах.
    """

    def __init__(self):
        """
        Инициализирует хелпер, загружая конфигурацию из .env файла.
        """
        load_dotenv()
        self.base_url = os.getenv("CURRENCY_API_URL")
        self.api_key = os.getenv("CURRENCY_API_KEY")

        if not self.base_url or not self.api_key:
            raise ValueError("Переменные CURRENCY_API_URL и CURRENCY_API_KEY должны быть установлены в .env файле")

        # Используем существующий currency.json как локальный кеш для списка валют
        self.currencies_cache_path = Path(__file__).parent / 'currency.json'
        self.currencies = self._load_currencies_from_cache()

    def _make_request(self, endpoint, params=None):
        """
        Внутренний метод для выполнения запросов к API.
        :param endpoint: Конечная точка API (например, 'convert', 'list').
        :param params: Словарь с параметрами запроса.
        :return: JSON-ответ от API в виде словаря или None при ошибке.
        """
        if params is None:
            params = {}

        # Добавляем ключ API к каждому запросу
        params['access_key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Вызовет исключение для кодов ошибок 4xx/5xx
            return response.json()
        except requests.exceptions.RequestException as e:
            # В реальном приложении здесь стоит добавить логирование
            print(f"Ошибка при запросе к API: {e}")
            return None

    def _load_currencies_from_cache(self):
        """Загружает список кодов валют из локального файла currency.json."""
        try:
            with open(self.currencies_cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Возвращаем только словарь { "USD": "United States Dollar", ... }
                return data.get("currencies", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def is_valid_currency(self, currency_code: str) -> bool:
        """
        Проверяет, является ли код валюты валидным, используя локальный кеш.
        Если кеш пуст, пытается его обновить через API.
        :param currency_code: Трехбуквенный код валюты (например, 'USD').
        :return: True, если валюта существует, иначе False.
        """
        if not self.currencies:
            self.update_currencies_cache()
        return currency_code.upper() in self.currencies

    def convert(self, from_currency: str, to_currency: str, amount: float = 1.0):
        """
        Конвертирует сумму из одной валюты в другую.
        :param from_currency: Код исходной валюты.
        :param to_currency: Код целевой валюты.
        :param amount: Сумма для конвертации.
        :return: Словарь с результатом конвертации или None в случае ошибки.
        """
        params = {
            'from': from_currency.upper(),
            'to': to_currency.upper(),
            'amount': amount
        }
        return self._make_request('convert', params=params)

    def update_currencies_cache(self):
        """
        Обновляет локальный кеш списка валют (currency.json), запрашивая данные из API.
        """
        print("Обновление кеша валют из API...")
        data = self._make_request('list')
        if data and data.get('success'):
            # Записываем полный ответ API в файл
            with open(self.currencies_cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.currencies = data.get('currencies', {})
            print("Кеш валют успешно обновлен.")
            return True
        print("Не удалось обновить кеш валют.")
        return False