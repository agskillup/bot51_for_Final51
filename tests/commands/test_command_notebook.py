# from bot.commands.command_notebook import NotebookCommand
#
# def test_notebook_add_note_and_list():
#     command = NotebookCommand()
#     user_id = 100
#     chat_id = 200
#
#     # Додаємо першу нотатку
#     res_add1 = command.execute('/notebook add First note', chat_id, user_id)
#     assert res_add1 == "Note added: First note"
#
#     # Додаємо другу нотатку
#     res_add2 = command.execute('/notebook add Second note', chat_id, user_id)
#     assert res_add2 == "Note added: Second note"
#
#     # Перевіряємо список нотаток
#     res_list = command.execute('/notebook list', chat_id, user_id)
#     assert res_list == "First note\nSecond note"
#
# def test_notebook_list_no_notes():
#     command = NotebookCommand()
#     user_id = 999
#     chat_id = 200
#     # Користувач не додав нотаток
#     res = command.execute('/notebook list', chat_id, user_id)
#     assert res == "No notes."
#
# def test_notebook_unknown_command():
#     command = NotebookCommand()
#     user_id = 100
#     chat_id = 200
#     res = command.execute('/notebook somethingelse', chat_id, user_id)
#     assert res == "Unknown notebook command."
