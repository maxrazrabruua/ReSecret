import os
import safe

def readfile(name):
    """
    Данная функция читает файл с именем заданым через переменную-аргумент возвращая соддержимое

    :param name: Имя файла для чтения(без расширения)
    :type name: str
    :return: соддержимое файла
    :rtype: str
    """    
    file_name = f"{name}.ps"
    
    if not os.path.exists(file_name):
        return f"Файл {file_name} не найден!"
    
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Ошибка при чтении файла {file_name}: {str(e)}"

vars = {}

def run(code):
    """
    Выполняет код языка программирования PythonScript(.ps)

    :param code: код на языке PythonScript
    :type code: str
    :return: None
    :rtype: None
    """
    i = 0
    for command in code.split("\n"):
        i += 1
        f, a = intepretator(command.split())
        if f is False:
            print(f"Ошибка на {i} строке: {a}")
            break

def printf(*args):
    """
    Функция создана для интепретатора вот что она выполняет:
    1. **Проверяет наличие есть ли переменная в списке vars если нет то выдаёт ошибку и завершает выполнение кода а иначе добавляет его значение**

    :param args: список аргументов т. е. переменные с $ перед ними или обычные слова
    :type args: tuple
    :return: успех или error
    :rtype: tuple
    """
    c = list(args)
    content = []
    for word in c:
        word = str(word) # Преобразуем в строку
        if word[0] == "$":
            if len(word) == 1:
                content.append(word)
            else:
                if word[1:] in vars.keys():
                    content.append(str(vars[word[1:]]))
                else:
                    return (False, f"Error: Variable '{word[1:]}' not found!")
        else:
            content.append(str(word))
    return (True, print(" ".join(content)))

def notspaceprint(*args):
    """
    Функция создана для интепретатора вот что она выполняет:
    1. **Проверяет наличие есть ли переменная в списке vars если нет то выдаёт ошибку и завершает выполнение кода а иначе добавляет его значение**

    :param args: список аргументов т. е. переменные с $ перед ними или обычные слова в отличие от printf() эта функция не добавляет пробелы между словами
    :type args: tuple
    :return: успех или error
    :rtype: tuple
    """
    c = list(args)
    content = ""
    for word in c:
        word = str(word) # Преобразуем в строку
        if word[0] == "$":
            if len(word) == 1:
                content += word
            else:
                if word[1:] in vars.keys():
                    content += str(vars[word[1:]])
                else:
                    return (False, f"Error: Variable '{word[1:]}' not found!")
        else:
            content += str(word)
    return (True, print(content))

# Это костыль
def costyl(a, b, op):
    """
    Это костыль для функции math (VSCode почему-то пошутил над функцией math())
    """
    l = {'a': a[1:] if a[0] == "$" else a, 'b': b[1:] if b[0] == "$" else b}
    l.update(vars) # Обновляем словарь l
    s = safe.Safe(l) # Создаём экземпляр класса Safe
    return s.mati(f"{a} {op} {b}") # Вызываем метод mati() и передаём туда строку с выражением

def costyl3(code):
    """
    Это костыль для костыля
    """
    try:
        return exec(code)
    except:
        return None

def costyl2(var, a, b, op):
    """
    Это костыль для функции math (логика)
    """
    types = []
    if a == "$":
        a = vars[a[1:]]
        types.append(type(a))
    else:
        try:
            int(a)
        except:
            pass
        else:
            if "." in a:
                a = float(a)
                types.append(float)
            else:
                a = int(a)
                types.append(int)
    
    if b == "$":
        b = vars[b[1:]]
        types.append(type(b))
    else:
        try:
            int(b)
        except:
            pass
        else: # Если это число
            if "." in b: # Если это число с плавающей точкой
                b = float(b) # Преобразуем во float
                types.append(float)
            else:
                b = int(b) # Если это целое число
                types.append(int)
    
    start = {
        "==": a == b,
        "!=": a != b
    }

    new = {
        "<": costyl3(f"{a} < {b}"),
        ">": costyl3(f"{a} > {b}"),
        "<=": costyl3(f"{a} <= {b}"),
        ">=": costyl3(f"{a} >= {b}")
    }

    note = start

    if str(types[0]) in ["[<class 'int'>]", "<class 'float'>"] or str(types[1]) in ["[<class 'int'>]", "<class 'float'>"]:
        note.update(new)
        if op in note.keys():
            vars[var] = note[op]
            return (True, note[op])
        else:
            return (False, "Error: Invalid operator")
    else:
        if op in note.keys():
            vars[var] = note[op]
            return (True, note[op])
        else:
            return (False, "Error: Invalid operator")

def math(var, a, b, op):
    global vars
    """
    Функция создана для интепретатора вот что она выполняет:
    1. **Проверяет наличие есть ли переменная в списке vars если нет то выдаёт ошибку и завершает выполнение кода а иначе добавляет его значение**
    2. **Проверяет наличие оператора который нужно использовать для выполнения операции если его нет то выдаёт ошибку и завершает выполнение кода а иначе выполняет операцию**

    :param a: первая переменная
    :type a: any
    :param b: вторая переменная
    :type b: any
    :param op: оператор который нужно использовать для выполнения операции
    :type op: str
    :param var: переменная в которую нужно записать результат
    :type var: str
    :return: успех или error
    :rtype: tuple
    """
    types = []
    sa = a
    sb = b
    for v in [a, b]:
        if v[0] == "$":
            if len(v) == 1:
                types.append(str)
            else:
                if v[1:] in vars.keys():
                    types.append(type(vars[v[1:]]))
                else:
                    return (False, f"Error: Variable '{v[1:]}' not found!")
        else:
            try:
                int(v)
            except:
                pass
            else: # Если это число
                if "." in v: # Если это число с плавающей точкой
                    v = float(v) # Преобразуем во float
                else:
                    v = int(v) # Если это целое число

            types.append(type(v))
    
    values = (a[1:], b[1:]) if a[0] == "$" and b[0] == "$" else (a[1:] if a[0] == "$" else a, b[1:] if b[0] == "$" else b)
    a, b = values
    note = {
        "[<class 'int'>, <class 'int'>]": {
            "+": costyl(a, b, "+"),
            "-": costyl(a, b, "-"),
            "*": costyl(a, b, "*"),
            "/": costyl(a, b, "/"),
            "%": costyl(a, b, "%"),
            "^": costyl(a, b, "**")
        },
        "[<class 'float'>, <class 'int'>]": {
            "+": costyl(a, b, "+"),
            "-": costyl(a, b, "-"),
            "*": costyl(a, b, "*"),
            "/": costyl(a, b, "/"),
            "^": costyl(a, b, "**")
        },
        "[<class 'int'>, <class 'float'>]": {
            "+": costyl(a, b, "+"),
            "-": costyl(a, b, "-"),
            "*": costyl(a, b, "*"),
            "/": costyl(a, b, "/"),
            "^": costyl(a, b, "**")
        },
        "[<class 'float'>, <class 'float'>]": {
            "+": costyl(a, b, "+"),
            "-": costyl(a, b, "-"),
            "*": costyl(a, b, "*"),
            "/": costyl(a, b, "/"),
            "^": costyl(a, b, "**")
        },
        "[<class 'str'>, <class 'str'>]": {
            "+": costyl(f"'{a}'", f"'{b}'", "+")
        },
        "[<class 'str'>, <class 'int'>]": {
            "+": costyl(f"'{a}'", str(b), "+"),
            "*": costyl(f"'{a}'", b, "*")
        },
        "[<class 'int'>, <class 'str'>]": {
            "+": costyl(str(a), f"'{b}'", "+")
        },
        "[<class 'float'>, <class 'str'>]": {
            "+": costyl(str(a), f"'{b}'", "+")
        }
    }

    strlist = str(types)
    if strlist in note.keys():
        if op in note[strlist].keys():
            vars[var] = note[strlist][op] # Записываем результат в переменную
            return (True, " ") # Возвращаем успех
        else:
            return costyl2(var, sa, sb, op) # Вызываем функцию costyl2() чтобы выполнить логическую операцию
    else:
        return (False, "Error: Invalid types")

def intepretator(com):
    """
    Сам интепретатор искающий команды выполняющих их задачу и возращающий успех или ошибку выполнения

    :param com: список аргументов которые состовляют эту самую команду
    :type com: list
    :return: успех или error
    :rtype: tuple
    """
    if len(com) == 0:
        return (True, " ")
    else:
        if com[0] == "print":
            if len(com) >= 2:
                return printf(*com[1:])
            else:
                return (False, "Error: Incorrect length")
        elif com[0] == "nsprint":
            if len(com) >= 2:
                return notspaceprint(*com[1:])
            else:
                return (False, "Error: Incorrect length")
        elif com[0] == "#":
            return (True, " ")
        elif com[0] == "set":
            if len(com) >= 5:
                if com[3] == "=":
                    startcom = " ".join(com[4:])
                    typevar = com[1]
                    if typevar == "str":
                        value = startcom
                    elif typevar == "int":
                        try:
                            value = int(startcom)
                        except:
                            return (False, "Error: Invalid value")
                    elif typevar == "float":
                        try:
                            value = float(startcom)
                        except:
                            return (False, "Error: Invalid value")
                    else:
                        return (False, "Error: Invalid type")
                    vars[com[2]] = value
                    return (True, " ")
                else:
                    return (False, "Error: Invalid syntax")
            else:
                return (False, "Error: Incorrect length")
        elif com[0] == "del":
            if len(com) == 2:
                if com[1] in vars.keys():
                    del vars[com[1]]
                    return (True, " ")
                else:
                    return (False, f"Error: Variable '{com[1]}' not found")
            else:
                return (False, "Error: Incorrect length")
        elif com[0] == "math":
            if len(com) == 6:
                if com[2] == "<=":
                    return math(com[1], com[3], com[5], com[4])
                else:
                    return (False, "Error: Invalid syntax")
            else:
                return (False, "Error: Incorrect length")
        else:
            return (False, "Error: Invalid command")
