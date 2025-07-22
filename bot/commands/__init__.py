# import os
# import importlib
# import inspect
# from bot.base import BotCommand
#
# def load_command_classes():
#     command_classes = {}
#     current_dir = os.path.dirname(__file__)
#     for file in os.listdir(current_dir):
#         if file.endswith(".py") and file not in ("__init__.py", "help_menu.py", "shutdown.py"):
#             module_name = file[:-3]
#             module = importlib.import_module(f".{module_name}", package=__name__)
#             for name, obj in inspect.getmembers(module):
#                 if inspect.isclass(obj) and issubclass(obj, BotCommand) and obj is not BotCommand:
#                     if module_name.startswith("command_"):
#                         command = module_name.removeprefix("command_")
#                     else:
#                         command = module_name
#                     command_classes[f"/{command}"] = obj
#                     break
#     return command_classes
#
# COMMAND_CLASSES = load_command_classes()
# COMMANDS = {k: v() for k, v in COMMAND_CLASSES.items()}

# Этот файл остается для того, чтобы Python считал 'commands' пакетом.
# Вся логика регистрации команд теперь явно находится в bot/factories.py.