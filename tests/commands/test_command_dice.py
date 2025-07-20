# from bot.commands.command_dice import DiceCommand, DiceStrategy
import pytest

# def test_dice_strategy_range(monkeypatch):
#     # Перевіряємо, що DiceStrategy повертає коректний діапазон (1-6)
#     results = set()
#     monkeypatch.setattr('bot.commands.command_dice.random.randint', lambda a, b: 4)
#     strategy = DiceStrategy()
#     for _ in range(10):
#         res = strategy.handle("any", 123, 42)
#         assert res == "🎲 You rolled: 4"
#         results.add(res)
#     assert results == {"🎲 You rolled: 4"}
#
# def test_dice_command_calls_strategy(monkeypatch):
#     # Перевіряємо, що DiceCommand делегує виклик у стратегію
#     monkeypatch.setattr('bot.commands.command_dice.random.randint', lambda a, b: 2)
#     cmd = DiceCommand()
#     out = cmd.execute("roll", 1, 1)
#     assert out == "🎲 You rolled: 2"
