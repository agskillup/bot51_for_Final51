from bot.base import BotCommand, CommandStrategy
from bot.helper.__temperature_helper import TemperatureHelper


class TemperatureStrategy(CommandStrategy):
    def handle(self, text, chat_id, user_id):

        if text.startswith('/temperature full'):
            command = '/temperature full'
            text = text.replace('/temperature full', '')
        else:
            command = '/temperature'
            text = text.replace('/temperature', '')

        # Значення за замовчуванням
        city = 'Odesa'
        units = 'metric'

        if text:
            parts = text.split()
            if len(parts) >= 1:
                city = parts[0]
            if len(parts) >= 2:
                units = parts[1]

        weather = TemperatureHelper(units=units)
        weather.fetch_weather(city)
        if command == '/temperature full':
            result = f"{city}: {weather.get_weather()}"
        else:
            result = f"{city}: {weather.get_temperature()}"
        return result


class TemperatureCommand(BotCommand):
    info = "Check the current temperature in a city (usage: <city> <units>)"

    def __init__(self):
        self.strategy = TemperatureStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
