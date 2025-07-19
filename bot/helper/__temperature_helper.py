import requests
import os
from dotenv import load_dotenv


class TemperatureHelper:
    def __init__(self, units='metric'):
        """
        Ініціалізуємо допоміжний клас для отримання температури.

        :param units: Система одиниць вимірювання: 'metric', 'imperial' або 'standard'
        """
        load_dotenv()
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.weather_url = os.getenv("WEATHER_URL")
        self.units = units
        self.data = {}

    def fetch_weather(self, city, **params):
        """
        Виконуємо запит погоди для конкретного міста.

        :param city: Назва міста
        :param params: Додаткові параметри для API
        """
        params['q'] = city
        params['appid'] = self.weather_api_key
        params.setdefault('units', self.units)
        response = requests.get(self.weather_url, params=params)
        response.raise_for_status()
        self.data = response.json()

    def get_temperature(self):
        """
        Повертає температуру у заданій системі одиниць.
        """
        temp = self.data.get('main', {}).get('temp')
        if temp is not None:
            unit_label = self._get_unit_label()
            return f"Температура: {temp} {unit_label}"
        return "Дані про температуру відсутні."

    def get_weather(self):
        """
        Повертає погоду і вологість.
        """
        humidity = self.data.get('main', {}).get('humidity')
        weather = self.data.get('weather', [{}])[0].get('main')
        if humidity is not None and weather is not None:
            unit_label = self._get_unit_label()
            return (f"Вологість: {humidity} \n"
                    f"Погода: {weather} ")
        return "Дані про вологість відсутні."

    def _get_unit_label(self):
        """
        Визначає позначення одиниць для температури.
        """
        if self.units == 'imperial':
            return '°F'
        elif self.units == 'standard':
            return 'K'
        else:
            return '°C'
