import os
import keyboard

ram = {
    "GLOBAL": {
        "local.nowOblast": "GLOBAL",
        "itp": "<component: itp>",
        "local": "<class: Local>",
        "raise": "<module: raise>",
        "console": "<class: Console>",
        "logCalls": [], # Прописка логов
        "timesCall": 0,
        "types": "<module: types>",
        "last": "\n"
    }
}

def itp(command: str):
    """Интерпретатор"""
    global ram
    if command == "":
        return None, True, "Нету ничего"
    else:
        ram["GLOBAL"]["timesCall"] += 1
        ram["GLOBAL"]["logCalls"].append(f"now oblast vars '{ram['GLOBAL']['local.nowOblast']}': call itp of {ram['GLOBAL']['timesCall']}times of command '{command}'")
        if ";" in command:
            strings = command.split(";")
            i = 0
            end = len(strings) - 1
            for string in strings:
                string = string.strip().lstrip()
                if end == i:
                    return itp(string)[0], True, "Мультистрок"
                else:
                    itp(string)
                    i += 1
        
        com = command.split(" ")
        try:
            test1 = com[1]
        except:
            test1 = "no"
    
    if com[0] == "//":
        return None, True, "Комментарий"
    elif com[0] == "echo":
        return print(itp(command[5:])[0], end=ram["GLOBAL"]["last"]), True, "Вывод"
    elif com[0] == "local.delOblast":
        oblast = itp(command[len("local.delOblast") + 1:])[0]
        if oblast != "GLOBAL":
            if oblast in ram.keys():
                if ram["GLOBAL"]["local.nowOblast"] == oblast:
                    ram["GLOBAL"]["local.nowOblast"] = "GLOBAL"
                del ram[oblast]
                return None, True, "Область переменных успешно удалена"
            else:
                return None, False, f"OblastError: Oblast vars '{oblast}' is not exists"
        else:
            return None, False, "OblastError: oblast vars 'GLOBAL' not deleting"
    elif com[0] == "local.vars":
        print("\n".join([f'{name}: {repr(value)}' for name, value in ram[ram["GLOBAL"]["local.nowOblast"]].items()]))
        return None, True, "Вывод всех переменных из данной области"
    elif com[0] == "local.globalization":
        ram["GLOBAL"]["local.nowOblast"] = "GLOBAL"
        return None, True, "Глобализация"
    elif com[0] == "local.set":
        if itp(command[10:])[0] in ram.keys():
            ram["GLOBAL"]["local.nowOblast"] = itp(command[10:])[0]
            return None, True, "Локализация"
        else:
            return None, False, f"OblastError: Oblast vars '{itp(command[10:])[0]}' is not exists"
    elif com[0] == "local.create":
        ram[itp(command[13:])[0]] = {
            "itp": "<component: itp>",
            "local": "<class: Local>",
            "raise": "<module: raise>",
            "console": "<class: Console>"
        }
        return None, True, "Область переменных была создана"
    elif com[0] == "local.import":
        if itp(command[13:])[0] in ram.keys():
            ram[itp(command[13:])[0]].update(ram[ram["GLOBAL"]["local.nowOblast"]])
            return None, True, "Импорт в другую область переменных"
        else:
            return None, False, f"OblastError: Oblast vars '{itp(command[13:])[0]}' is not exists"
    elif com[0] == "local.var":
        if itp(com[1])[0] in ram.keys() and itp(com[2])[0] in ram[ram["GLOBAL"]["local.nowOblast"]].keys():
            ram[itp(com[1])[0]][itp(com[2])[0]] = ram[ram["GLOBAL"]["local.nowOblast"]][itp(com[2])[0]]
            return None, True, "Импорт в другую область переменных"
        elif not itp(com[2])[0] in ram[ram["GLOBAL"]["local.nowOblast"]].keys():
            return None, False, f"NameError: '{command}' is not diclared in {ram['GLOBAL']['local.nowOblast']} oblast vars"
        else:
            return None, False, f"OblastError: Oblast vars '{itp(com[1])[0]}' is not exists"
    elif com[0] == "raise.debug":
        result = itp(itp(command[(len("raise.debug") + 1):])[0])[2]
        return result, True, "Дебаг"
    elif com[0] == "itp.ram":
        print(ram)
        return None, True, "Вывод памяти"
    elif com[0] == "itp.exec":
        itp(itp(command[9:])[0])
        return None, True, "Выполнение"
    elif com[0] == "itp.eval":
        return itp(itp(command[9:])[0])[0], True, "Вывод"
    elif com[0] == "console.clear":
        os.system("cls")
        return None, True, "Очистка экрана"
    elif com[0] == "console.plus":
        print('\n' * 1024)
        return None, True, "plus"
    elif com[0] == "console.start":
        ram["GLOBAL"]["last"] = "\r"
        return None, True, "start"
    elif com[0] == "types.str":
        return str(itp(command[10:]))[0], True, "Тайпинг стринг"
    elif com[0] == "types.int":
        try:
            return (int(float(itp(command[10:])[0])) if command[10:] not in ['False', 'True'] else ['False', 'True'].index(command[10:])) if not isinstance(itp(command[10:])[0], bool) else int(itp(command[10:])[0]), True, "Тайпинг инт"
        except:
            return None, False, "ValueError: typing-operation ANY in INT is not working"
    elif com[0] == "types.float":
        try:
            return float(itp(command[10:])[0]), True, "Тайпинг флоэт"
        except:
            return None, False, "ValueError: typing-operation ANY in FLOAT is not working"
    elif com[0] == "types.list":
        try:
            return list(itp(command[10:])[0]), True, "Тайпинг лист"
        except:
            return None, False, "ValueError: typing-operation ANY in LIST is not working"
    elif com[0] == "types.bool":
        try:
            return bool(itp(command[10:])[0]), True, "Тайпинг буле"
        except:
            return None, False, "ValueError: typing-operation ANY in BOOL is not working"
    elif com[0] == "types.repr":
        getting = itp(command[11:])[0]
        if isinstance(getting, str):
            return '"' + str(getting) + '"', True, "repr"
        elif isinstance(getting, list):
            new = []
            for element in str(getting)[1:-1].split(","):
                result = itp(element[1:-1] if element[0] == "[" and element[-1] == "]" else element)[0]
                new.append('"' + result + '"' if isinstance(result, str) else str(result)) if not itp(element)[0] is None else ''
            else:
                return new, True, "repr"
        else:
            return repr(getting), True, "else repr"
    elif com[0] == "range":
        try:
            return list(range(itp(command[6:])[0])), True, "range"
        except:
            return False, False, "SyntaxError: maybe len args <"
    elif com[0] == "for":
        try:
            args = command[4:].split(": ")
            new = args[0]
            start = itp(args[1])[0]
            c = itp(args[2])[0]
            itp("local.create \"for\"")
            itp("local.import \"for\"")
            itp("local.set \"for\"")
            for i in start:
                itp("local.set \"for\"")
                itp(f"{new} = {i}")
                itp(c)
            else:
                itp("local.delOblast \"for\"")
                ram["GLOBAL"]["last"] = "\n"
                print('\n')
            return True, True, "for"
        except:
            return False, False, "SyntaxError: maybe len args <"
    elif com[0] == "while":
        try:
            while True:
                if not (keyboard.is_pressed("end") or keyboard.is_pressed("esc")):
                    args = command[6:].split(", ")
                    cod = itp(args[0])[0]
                    true = itp(args[1])[0]
                    if cod:
                        itp(true)
                    else:
                        break
                else:
                    break
            return True, True, "while"
        except:
            return False, False, "SyntaxError: maybe len args <"
    elif com[0] == "if":
        try:
            args = command[3:].split(", ")
            cod = itp(args[0])[0]
            true = itp(args[1])[0]
            try:
                false = itp(args[2])[0]
            except:
                false = ""
            if cod:
                itp(true)
            else:
                itp(false)
            return True, True, "ifing"
        except:
            return False, False, "SyntaxError: maybe len args <"
    elif com[0] == "split":
        try:
            args = command[6:].split(", ")
            return itp(args[0])[0].split(itp(args[1])[0]), True, "spliting"
        except:
            return [], False, "TypeError: ANY not supported 'split' maybe STR or LIST?"
    elif com[0] == "join":
        try:
            args = command[5:].split(", ")
            return itp(args[1])[0].join(itp(args[0])[0]), True, "spliting"
        except:
            return "", False, "TypeError: ANY not supported 'join' maybe LIST to 1 arg or STR to 2 arg?"
    elif com[0] == "not":
        op = "not"
        try:
            one = command[4:]
            return not (itp(one.lstrip())[0]), True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "or":
        op = "or"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return one or two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "xor":
        op = "xor"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return not (one or two), True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "xand":
        op = "xand"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return not (one and two), True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "and":
        op = "and"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return one and two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "==":
        op = "=="
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one == two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "!=":
        op = "!="
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 3):])[0]
            return one != two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == ">":
        op = ">"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one > two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == ">=":
        op = ">="
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return one >= two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "<":
        op = "<"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return one < two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "<=":
        op = "<="
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + len(op) + 1):])[0]
            return one <= two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "+":
        op = "+"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one + two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "-":
        op = "-"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one - two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "/":
        op = "/"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one / two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "//":
        op = "//"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 3):])[0]
            return one // two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "*":
        op = "*"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one * two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "%":
        op = "%"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 2):])[0]
            return one % two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    elif test1 == "**":
        op = "**"
        try:
            one, two = itp(command.split(op)[0].strip())[0], itp(command[(len(command.split(op)[0]) + 3):])[0]
            return one ** two, True, op
        except:
            return False, False, f"TypeError: is type not supported operator: {op}"
    else:
        try:
            int(float(command))
        except:
            if command[0] == '"' and command[-1] == '"':
                return command[1:-1].replace("\\n", "\n").replace("\\c", ";").replace("\\z", ",").replace("\\d", ":"), True, "Строка"
            else:
                try:
                    if not "=" in command:
                        if not command[0] == "[" and not command[:-1] == "]":
                            if command not in ["False", "True"]:
                                return ram[ram["GLOBAL"]["local.nowOblast"]][command], True, "Переменная"
                            else:
                                return command == 'True', True, "bool"
                        else:
                            new = []
                            for element in command[1:-1].split(","):
                                new.append(itp(element[1:-1] if element[0] == "[" and element[-1] == "]" else element)[0]) if not itp(element)[0] is None else ''
                            else:
                                return new, True, "Список"
                    else:
                        kv = command.split("=")
                        ram[ram["GLOBAL"]["local.nowOblast"]][kv[0].strip()] = itp(kv[1].lstrip())[0]
                        return None, True, "Объявление переменной"
                except KeyError:
                    return None, False, f"NameError: '{command}' is not diclared in {ram['GLOBAL']['local.nowOblast']} oblast vars"
        else:
            if "." in command:
                return float(command), True, "Дробь"
            else:
                return int(command), True, "Не дробь"

while True:
    result, a, b = itp(input(">>> "))
    print("<<<", result)
