# from bot.commands.command_iam import IAmCommand, IAmStrategy
#
# def test_iam_strategy_formats_output():
#     s = IAmStrategy()
#     out = s.handle("irrelevant", chat_id=55, user_id=101)
#     assert out == "Your ID: 101, chat: 55"
#
# def test_iam_command_executes():
#     cmd = IAmCommand()
#     r = cmd.execute("doesn't matter", 11, 9)
#     assert "Your ID: 9" in r
#     assert "chat: 11" in r
