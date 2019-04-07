"""
Рассматривается грамматика логических выражений с правилами
<выражение> -> <логическое выражение>
<логическое выражение> -> <логический одночлен> | <логическое выражение> ! <логический одночлен>
<логический одночлен> -> <вторичное логическое выражение> | <логический одночлен> & <вторичное логическое выражение>
<вторичное логическое выражение> -> <первичное логическое выражение> | ~ <первичное логическое выражение>
<первичное логическое выражение> -> <логическое значение> | <идентификатор>
<логическое значение> -> true | false
<знак логической операции> -> ~ | & | !
Замечания.
1. Нетерминал <идентификатор> - это лексическая единица (лексемы), которая оставлена
неопределенной, а при выполнении лабораторной работы можно либо рассматривать ее как
терминальный символ, либо определить ее по своему усмотрению и добавить это
2. определение.
3. Терминалы true, false - ключевые слова (зарезервированные).
4. Терминалы ~ | & | ! - это знаки операций.
5. Нетерминал <выражение> - это начальный символ грамматики.

Дополнить грамматику блоком, состоящим из последовательности операторов присваивания. Для реализации
предлагаются два варианта расширенной грамматики.
"""

i = 0           # Текущее положение входной головки
err_flag = 0    # Флаг, фиксирующий наличие ошибок в середине правила
string = []    # Строка с входной цепочкой, имитирующая входную лентуСтрока с входной цепочкой, имитирующая входную ленту
alph = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(' ')


def parse(inp):
    """
    Парсинг строки на соответсиве грамматики через реккурсивынй спуск
    :type inp: str
    :return: True если соответсвует, False иначе
    """
    global string, i, err_flag
    i = 0
    err_flag = 0
    string = inp.split(' ')
    while i < len(string):
        if not is_expression():
            return False


def is_expression():
    """
    Проверка <выражение>
    :return:
    """
    global err_flag
    if is_logical_expression():
        return True
    else:
        err_flag = err_flag + 1
        return False


def is_logical_expression():
    """
    Проверка <логическое выражение>
    """
    global i, err_flag, string
    if is_logical_monomial():
        return True
    elif is_logical_expression():
        if string[i] == '!':
            i = i + 1
            if is_logical_monomial():
                return True
            else:
                err_flag = err_flag + 1
                return False
        else:
            err_flag = err_flag + 1
            return False
    else:
        err_flag = err_flag + 1
        return False


def is_logical_monomial():
    """
    Проверка <логический одночлен>
    """
    global i, err_flag, string
    if is_second_logical_expression():
        return True
    elif is_logical_monomial():
        if string[i] == '&':
            i = i + 1
            if is_second_logical_expression():
                return True
            else:
                err_flag = err_flag + 1
                return False
        else:
            err_flag = err_flag + 1
            return False
    else:
        err_flag = err_flag + 1
        return False


def is_second_logical_expression():
    """
    Проверка <второе логическое выражение>
    """
    global i, string, err_flag
    if is_first_logical_expression():
        return True
    elif string[i] == '~':
        i = i + 1
        if is_first_logical_expression():
            return True
        else:
            err_flag = err_flag + 1
            return False
    else:
        err_flag = err_flag + 1
        return False


def is_first_logical_expression():
    """
    Проверка <первичное логическое выражение>
    """
    global err_flag
    if is_logical_value() or is_identifier():
        return True
    else:
        err_flag = err_flag + 1
        return False


def is_logical_value():
    """
    Проверка <логическое значение>
    """
    global i, string, err_flag
    if string[i] in ['true', 'false']:
        i = i + 1
        return True
    else:
        err_flag = err_flag + 1
        return False


def is_identifier():
    global i, string, err_flag
    if string[i] in alph:
        i = i + 1
        return True
    else:
        err_flag = err_flag + 1
        return False
