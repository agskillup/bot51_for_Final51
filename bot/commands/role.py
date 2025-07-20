# Файл `role.py` - мощный административный инструмент.
# Он не выполняет бизнес-логику сам, а выступает в роли
# защищённого и умного диспетчера**, который парсит запросы
# администратора и делегирует их выполнение специализированным
# обработчикам (стратегиям). Это ядро системы безопасности и
# управления правами пользователей.

import os
from dotenv import load_dotenv
from bot.base import BotCommand

# Імпортуємо глобальні словники
from bot.roles.commands import commands_dict
from bot.roles.users import users_dict

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

class RoleStrategy:
    def execute(self, parts):
        raise NotImplementedError

class RoleDeleteStrategy(RoleStrategy):
    def execute(self, parts):
        # /role <role> delete
        role = parts[1]
        if role in users_dict:
            del users_dict[role]
            return f"Роль '{role}' видалена з users_dict."
        return f"Роль '{role}' не знайдена в users_dict."

class RoleAddStrategy(RoleStrategy):
    def execute(self, parts):
        # /role add <role>
        role = parts[2]
        if role in users_dict:
            return f"Роль '{role}' вже існує в users_dict."
        users_dict[role] = []
        return f"Роль '{role}' додана в users_dict."

class RoleRemoveStrategy(RoleStrategy):
    def execute(self, parts):
        # /role remove <role>
        role = parts[2]
        if role in users_dict:
            del users_dict[role]
            return f"Роль '{role}' видалена з users_dict."
        return f"Роль '{role}' не знайдена в users_dict."

class RoleAddToStrategy(RoleStrategy):
    def execute(self, parts):
        # /role add to <role> <id>
        role = parts[3]
        uid = int(parts[4])
        if role not in users_dict:
            return f"Роль '{role}' не існує в users_dict."
        if uid in users_dict[role]:
            return f"ID {uid} вже у ролі '{role}'."
        users_dict[role].append(uid)
        return f"ID {uid} додано до ролі '{role}'."

class RoleRemoveFromStrategy(RoleStrategy):
    def execute(self, parts):
        # /role remove from <role> <id>
        role = parts[3]
        uid = int(parts[4])
        if role not in users_dict or uid not in users_dict[role]:
            return f"ID {uid} немає у ролі '{role}'."
        users_dict[role].remove(uid)
        return f"ID {uid} видалено з ролі '{role}'."

class RoleShowStrategy(RoleStrategy):
    def execute(self, parts):
        # /role show users
        if len(parts) == 3 and parts[1] == "show" and parts[2] == "users":
            if not users_dict:
                return "Жодної ролі не знайдено."
            res = ["Користувачі за ролями:"]
            for role, users in users_dict.items():
                users_list = ", \n".join(str(u) for u in users) if users else "немає"
                res.append(f"  {role}: {users_list}")
            return "\n".join(res)

        # /role show commands
        if len(parts) == 3 and parts[1] == "show" and parts[2] == "commands":
            if not commands_dict:
                return "Жодної команди не знайдено."
            res = ["Команди та ролі:"]
            for cmd, roles in commands_dict.items():
                roles_list = ", \n".join(roles) if roles else "немає ролей"
                res.append(f"  {cmd}: {roles_list}")
            return "\n".join(res)
        return "Невідома команда show. Доступно: users, commands."

class RoleCommand(BotCommand):
    def __init__(self):
        self.strategies = {
            "delete": RoleDeleteStrategy(),
            "add": RoleAddStrategy(),
            "remove": RoleRemoveStrategy(),
            "add_to": RoleAddToStrategy(),
            "remove_from": RoleRemoveFromStrategy(),
            "show": RoleShowStrategy()
        }

    def execute(self, text, chat_id, user_id, **kwargs):
        if str(user_id) != str(ADMIN_ID):
            return "Access denied."
        parts = text.strip().split()
        if len(parts) < 2:
            return "Invalid command. Usage: /role ..."

        # /role <role> delete
        if len(parts) == 3 and parts[2] == "delete":
            return self.strategies["delete"].execute(parts)
        # /role add <role>
        if parts[1] == "add" and len(parts) == 3:
            return self.strategies["add"].execute(parts)
        # /role remove <role>
        if parts[1] == "remove" and len(parts) == 3:
            return self.strategies["remove"].execute(parts)
        # /role add to <role> <id>
        if parts[1] == "add" and parts[2] == "to" and len(parts) == 5:
            return self.strategies["add_to"].execute(parts)
        # /role remove from <role> <id>
        if parts[1] == "remove" and parts[2] == "from" and len(parts) == 5:
            return self.strategies["remove_from"].execute(parts)

        # /role show users
        if parts[1] == "show" and len(parts) == 3:
            return self.strategies["show"].execute(parts)

        return "Невірний синтаксис. Дивись інструкцію."
