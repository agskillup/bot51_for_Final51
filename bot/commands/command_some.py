import requests
from bot.base import BotCommand, CommandStrategy

class SomeStrategy(CommandStrategy):
    def handle(self, text, chat_id, user_id):
        print("Hello {}".format(text))
        return "Some command"
        # try:
        #     url = f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        #     resp = requests.get(url, timeout=5)
        #     resp.raise_for_status()
        #     data = resp.json()
        #     if data and isinstance(data, dict):
        #         result = f"Currency: {data['symbol']} Amount: {data['price']}"
        #         print(result,1)
        #         return result
        #     # Якщо порожній словник або не словник
        #     print(2)
        #     return None
        # except Exception as e:
        #     print(3,e)
        #     return None


class SomeCommand(BotCommand):
    def __init__(self):
        self.strategy = SomeStrategy()

    def execute(self, text, chat_id, user_id):
        return self.strategy.handle(text, chat_id, user_id)
