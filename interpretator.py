import os
import keyboard
import time

class Module:
    """Модуль"""
    def __init__(self, name: str, oblast: dict):
        self.name = name
        self.oblast = oblast
    
    def __getitem__(self, key: str):
        return self.oblast[key]
    
    def __setitem__(self, key: str, value: object):
        self.oblast[key] = value
    
    def __repr__(self):
        return str(f"<Module: {self.name}>")
    
    def __str__(self):
        return "<class: Module>"

ram = {
    "GLOBAL": {
        "local.nowOblast": "GLOBAL",
        "itp": "<component: itp>",
        "local": "<class: local>",
        "raise": "<module: raise>",
        "console": "<class: console>",
        "logCalls": [], # Прописка логов
        "timesCall": 0,
        "types": "<module: types>",
        "last": "\n",
        "cash": {},
        "module": "<class: module>"
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
    elif com[0] == "module.import":
        try:
            nameModule = itp(command[14:])[0]
            try:
                with open(f"{nameModule}.ards", "r", encoding="utf-8") as file:
                    content = file.read()
            except:
                try:
                    with open(f"{nameModule}.ard", "r", encoding="utf-8") as file:
                        content = file.read()
                except:
                    return None, False, f"ModuleError: '{nameModule}' not found"

            oblast = run(content, file=nameModule)
            ram[nameModule] = oblast
            return None, True, "Импорт модуля"
        except:
            return None, False, "TypeError: name of module should be STR"
    elif com[0] == "module.zip":
        try:
            nameModule = itp(command[11:])[0]
            try:
                with open(f"{nameModule}.ards", "r", encoding="utf-8") as file:
                    content = file.read()
            except:
                try:
                    with open(f"{nameModule}.ard", "r", encoding="utf-8") as file:
                        content = file.read()
                except:
                    return None, False, f"ModuleError: '{nameModule}' not found"
            oblast = run(content, file=nameModule)
            return Module(nameModule, oblast), True, "Зиппинг модуля"
        except:
            return None, False, "TypeError: name of module should be STR"
    elif com[0] == "module.name":
        obj = itp(command[12:])[0]
        if isinstance(obj, Module):
            return obj.name, True, "Имя модуля"
        else:
            return "", False, "TypeError: command 'module.name' not supported for not MODULES"
    elif com[0] == "module.extract":
        obj = itp(command[15:])[0]
        if isinstance(obj, Module):
            ram[obj.name] = obj.oblast
            return None, True, "Распаковочка"
        else:
            return None, False, "TypeError: command 'module.extract' not supported for not MODULES"
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
    elif com[0] == "local.export":
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
            return None, False, f"NameError: '{itp(com[2])[0]}' is not diclared in {ram['GLOBAL']['local.nowOblast']} oblast vars"
        else:
            return None, False, f"OblastError: Oblast vars '{itp(com[1])[0]}' is not exists"
    elif com[0] == "raise.debug":
        try:
            result = itp(itp(command[(len("raise.debug") + 1):])[0])[2]
            return result, True, "Дебаг"
        except:
            return "FormatError: problem of format", True, "Дебаг"
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
    elif com[0] == "stop":
        try:
            return time.sleep(itp(command[5:])[0]), True, "stopped"
        except:
            return None, False, "TypeError: arg should be FLOAT"
    elif com[0] == "range":
        try:
            return list(range(itp(command[6:])[0])), True, "range"
        except:
            return False, False, "SyntaxError: maybe len args <"
    elif com[0] == "for":
        try:
            args = command[4:].split(": ")
            new = []
            start = []
            for value in args[1].split("^"):
                start.append(itp(value)[0])
            
            for var in args[0].split("^"):
                new.append(var)
            
            itp("local.create \"for\"")
            itp("local.import \"for\"")
            itp("local.set \"for\"")
            try:
                ram["cash"] = {}
            except Exception as e:
                print(f"{e.__class__.__name__}: {str(e)}")
            ram["cash"]["LEN"] = len(start[0])
            for i in range(ram["cash"]["LEN"]):
                if not (keyboard.is_pressed("end") or keyboard.is_pressed("esc")):
                    if "T" not in ram["cash"].keys():
                        ram["cash"]["T"] = {}
                        for x in range(ram["cash"]["LEN"]):
                            for n in new:
                                if n in ram["cash"].keys():
                                    getindex = ram["cash"][n]
                                else:
                                    getindex = new.index(n)
                                    ram["cash"][n] = getindex
                                if n not in ram["cash"]["T"].keys():
                                    ram["cash"]["T"][n] = [start[getindex][x]]
                                else:
                                    ram["cash"]["T"][n].append(start[getindex][x])
                    for k, v in ram["cash"]["T"].items():
                        itp(f"{k} = {v[i] if not isinstance(v[i], str) else '"' + v[i] + '"'}")
                    else:
                        itp(itp(args[2])[0])
                else:
                    break
            else:
                itp("local.delOblast \"for\"")
                ram["GLOBAL"]["last"] = "\n"
                print('\n')
                ram["cash"].clear()
            return True, True, "for"
        except Exception as e:
            print(f"{e.__class__.__name__}: {str(e)}")
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
    elif com[0] == "reverse":
        try:
            return itp(command[8:])[0][::-1], True, "Вывод перевёрного списка или перевёрнотой строки"
        except:
            return [], False, "TypeError: ANY not supported 'reverse' maybe STR or LIST?"
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
    elif com[0] == "dict":
        try:
            args = command[5:].split(": ")
            keys = itp(args[0])[0]
            values = itp(args[1])[0]
            return {k: v for k, v in zip(keys, values)}, True, "Создание словаря"
        except:
            return {}, False, "TypeError: 2 args should be LISTs and not ANYs(not LISTs)"
    elif com[0] == "value":
        args = command[6:].split(": ")
        if len(args) < 2:
            return None, False, f"LenError: now {len(args)} args, should be 2 args!"
        central = itp(args[0])[0]
        index = itp(args[1])[0]
        if isinstance(central, dict):
            try:
                return central[index], True, "Индексирование словаря"
            except:
                return None, False, f"KeyError: '{index}' not in dict"
        elif isinstance(central, (str, list)):
            if isinstance(index, int):
                try:
                    return central[index], True, "Индексирование несловарного элемента"
                except:
                    return None, False, f"IndexError: '{str(index)}' not in iterable-element"
            else:
                return None, False, "TypeError: index-iteralbe not dict(and module) should be INT and not ANY(not INT)"
        elif isinstance(central, Module):
            if isinstance(index, str):
                try:
                    return central[index], True, "Индексирование модуля"
                except:
                    return None, False, f"VarError: '{index}' not in module"
            else:
                return None, False, f"TypeError: index-module should be STR and not ANY(not STR)"
        else:
            return None, False, "TypeError: ANY should be iterable and not literable"
    elif com[0] == "set":
        args = command[4:].split(": ")
        if len(args) < 3:
            return None, False, f"LenError: now {len(args)} args, should be 3 args!"
        central = itp(args[0])[0]
        index = itp(args[1])[0]
        value = itp(args[2])[0]
        if isinstance(central, dict):
            central[index] = value
            return central, True, "Индексирование словаря"
        elif isinstance(central, (str, list)):
            if isinstance(index, int):
                try:
                    central[index] = value
                    return central, True, "Индексирование несловарного элемента"
                except:
                    return None, False, f"IndexError: '{str(index)}' not in iterable-element"
            else:
                return None, False, "TypeError: index-iteralbe not dict should be INT and not ANY(not INT)"
        elif isinstance(central, Module):
            if isinstance(index, str):
                central[index] = value
                return central, True, "Индексирование модуля"
            else:
                return None, False, f"TypeError: index-module should be STR and not ANY(not STR)"
        else:
            return None, False, "TypeError: ANY should be iterable and not literable"
    elif com[0] == "append":
        args = command[7:].split(": ")
        if len(args) < 2:
            return None, False, f"LenError: now {len(args)} args, should be 2 args!"
        central = itp(args[0])[0]
        appending = itp(args[1])[0]
        if isinstance(central, list):
            return central + [appending], True, "append"
        else:
            return [], False, "TypeError: parent is not LIST, should be LIST"
    elif com[0] == "remove":
        args = command[7:].split(": ")
        if len(args) < 2:
            return None, False, f"LenError: now {len(args)} args, should be 2 args!"
        central = itp(args[0])[0]
        removing = itp(args[1])[0]
        if isinstance(central, list):
            try:
                central.remove(removing)
                return central, True, "remove"
            except:
                return central, True, "remove"
        else:
            return [], False, "TypeError: parent is not LIST, should be LIST"
    elif com[0] == "keys":
        try:
            return itp(command[5:])[0].keys(), True, "Ключики"
        except:
            return [], False, "TypeError: element is not DICT"
    elif com[0] == "values":
        try:
            return itp(command[7:])[0].values(), True, "Значения"
        except:
            return [], False, "TypeError: element is not DICT"
    elif com[0] == "len":
        try:
            el = command[4:]
            return len(itp(el)[0]), True, "lenning"
        except:
            return 0, False, "TypeError: ANY should be iterable and not literable"
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
                return command[1:-1].replace("\\n", "\n").replace("\\c", ";").replace("\\z", ",").replace("\\k", ":").replace("\\a", "^"), True, "Строка"
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
                            for element in command[1:-1].split(", "):
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

def terminal():
    global ram
    ram = {
        "GLOBAL": {
            "local.nowOblast": "GLOBAL",
            "itp": "<component: itp>",
            "local": "<class: local>",
            "raise": "<module: raise>",
            "console": "<class: console>",
            "logCalls": [], # Прописка логов
            "timesCall": 0,
            "types": "<module: types>",
            "last": "\n"
        }
    }
    while True:
        result, a, b = itp(input(">>> "))
        print("<<<", result)

def run(code: str, finishMessage: bool = False, file: str = "MAIN"):
    global ram
    ram = {
        "GLOBAL": {
            "local.nowOblast": "GLOBAL",
            "itp": "<component: itp>",
            "local": "<class: local>",
            "raise": "<module: raise>",
            "console": "<class: console>",
            "logCalls": [], # Прописка логов
            "timesCall": 0,
            "types": "<module: types>",
            "last": "\n",
            "cash": {},
            "module": "<class: module>"
        }
    }
    i = 0
    for command in code.split("\n"):
        i += 1
        _, a, b = itp(command)
        if not a:
            print(f"error in file '{file}' of {i} line:\n")
            print(f"  -> {command}:")
            print(f"  << {b}")
            break
    else:
        if finishMessage:
            print("\n[Programm finished]\n")
            print("logs:")
            print("\n".join(ram["GLOBAL"]["logCalls"]))
    return ram["GLOBAL"]
