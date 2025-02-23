class Safe:
    def __init__(self, vars=None):
        if vars is None:
            self.vars = {}
        else:
            self.vars = vars

    def var(self, name, value):
        """Добавить переменную в словарь, проверив тип."""
        if type(value) in [int, float]:
            self.vars[name] = value
        else:
            raise TypeError("Variable must be of type int or float.")

    def delVar(self, name):
        """Удалить переменную по имени."""
        if name in self.vars:
            del self.vars[name]
        else:
            raise ValueError(f"Variable '{name}' not found.")

    def mati(self, value, error=True):
        """Оценка выражений с переменными и числовыми операциями."""
        vars = []
        newMat = ""
        literTrue = False
        varName = ""
        
        for s in value:
            # Проверка на допустимые символы
            if s not in "0123456789*+/-.'_()%$ qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
                if not error:
                    return
                else:
                    print(s)
                    raise ValueError("Invalid symbol. Allowed: numbers, operators, variables, and _ .")
            
            # Если это буква, начинаем собирать имя переменной
            elif s.isalpha():
                if literTrue:
                    varName += s
                else:
                    literTrue = True
                    varName = s
            # Если символ - это не буква, проверяем и добавляем значение переменной
            elif literTrue:
                if varName in self.vars:
                    newMat += str(self.vars[varName])
                else:
                    raise ValueError(f"Variable '{varName}' is not defined.")
                literTrue = False
                newMat += s
            else:
                newMat += s
        
        # Если в конце есть собранная переменная, добавляем её
        if literTrue:
            if varName in self.vars:
                newMat += str(self.vars[varName]).replace("(", "").replace(")", "")
            else:
                raise ValueError(f"Variable '{varName}' is not defined.")

        # Выполнение вычисления с помощью eval
        try:
            return eval(newMat)
        except Exception as e:
            return 0
