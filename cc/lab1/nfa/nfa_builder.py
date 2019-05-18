import copy

from nfa.fa import Automata
from nfa.fa_state import State

NAME = 0


def build_nfa(regexp: str):
    """
    Построение НКА по регулярному выражению
    :param regexp: Регулярное выражение
    :return: НКА
    """
    # Стек. Содержит либо символы операторов, либо промежуточные КА в виде кортежа:
    # (startState, finalStates), finalStates: list
    global NAME
    fa_stack = list()
    for char in regexp:
        if char == '(' or char == '|':
            # Если встретили скобку, то надо сначала собрать автомат по тому, что внутри скобок.
            # Если встретили бинарный оператор, то он нам пригодится потом
            fa_stack.append(char)
        elif char == '*':
            # Унарный оператор. Берем верхний автомат из стека и модифицируем его
            build_zero_iter(fa_stack)
        elif char == '+':
            build_one_inter(fa_stack)
        elif char == ')':
            # Закрыли скобку. Надо получившийся в скобке автомат тоже модифицировать, если перед скобками что-то было
            close_group(fa_stack)
        else:
            # У нас тут просто буква
            new_start = State(str(NAME))
            NAME = NAME + 1
            new_end = State(str(NAME))
            NAME = NAME + 1
            new_end.isFinalState = True
            new_start.moveOnChar(char, new_end)
            build_operators(fa_stack, new_start, [new_end])
    start, _ = fa_stack.pop()
    return Automata(startState=start)


def build_zero_iter(stack: list):
    """
    Построение автомата для итерации 0 или больше
    :param stack: стек автоматов
    """
    global NAME
    new_star = State(str(NAME))
    NAME = NAME + 1
    new_end = State(str(NAME))
    NAME = NAME + 1
    new_end.isFinalState = True
    last_start, last_finals = stack.pop()
    new_star.moveOnEpsilon(last_start)
    new_star.moveOnEpsilon(new_end)
    for state in last_finals:
        state.isFinalState = False
        state.moveOnEpsilon(last_start)
        state.moveOnEpsilon(new_end)
    stack.append((new_star, [new_end]))


def build_one_inter(stack: list):
    """
    Построение автомата для итерации 1 и больше
    :param stack:
    """
    global NAME
    top_copy = copy.deepcopy(stack[-1])
    top_copy[0].positions = str(NAME)
    NAME = NAME + 1
    for state in top_copy[1]:
        state.positions = str(NAME)
        NAME = NAME + 1
    build_zero_iter(stack)
    iter_start, iter_ends = stack.pop()
    stack.append(top_copy)
    build_multiple(stack, iter_start, iter_ends)


def build_sum(stack, start_state, final_states):
    """
    Построение оператора a|b
    :param stack: стек автоматов
    :param start_state: начальное состояние автомата b
    :param final_states: конечные состояния автомата b
    """
    global NAME
    new_start = State(str(NAME))
    NAME = NAME + 1
    new_end = State(str(NAME))
    NAME = NAME + 1
    new_end.isFinalState = True

    a_start, a_finals = stack.pop()

    new_start.moveOnEpsilon(a_start)
    new_start.moveOnEpsilon(start_state)

    state: State
    for state in final_states:
        state.moveOnEpsilon(new_end)
        state.isFinalState = False
    for state in a_finals:
        state.moveOnEpsilon(new_end)
        state.isFinalState = False
    stack.append((new_start, [new_end]))


def build_multiple(stack, start_state, final_states):
    """
    Построение оператора a*b
    :param stack: стек автоматов
    :param start_state: начальное состояние автомата b
    :param final_states: конечные состояния автомата b
    """
    a_start, a_finals = stack.pop()
    for state in a_finals:
        state.isFinalState = False
        state.charTransitions = start_state.charTransitions
        state.epsilonTransitions = start_state.epsilonTransitions
    stack.append((a_start, final_states))


def close_group(stack: list):
    """
    Закрытие скобки
    :param stack: стек автоматов
    """
    global NAME
    last_start, last_finals = stack.pop()   # Автомат того, что было в скобках
    stack.pop()                             # Избовляемся от скобки в стеке
    build_operators(stack, last_start, last_finals)


def build_operators(stack, start_state, final_states):
    """
    Построение бинарных операторов типа a|b
    :param stack: стек автоматов
    :param start_state: начальное состояние автомата b
    :param final_states: конечные состояния автомата b
    """
    if len(stack) > 0 and stack[-1] != '(':
        operation = stack[-1]
        if isinstance(operation, str) \
                and operation == '|':      # В стеке может быть только операция |, т.к. обычно в регулярках . не пишут
            stack.pop()
            build_sum(stack, start_state, final_states)
        else:
            build_multiple(stack, start_state, final_states)
    else:
        stack.append((start_state, final_states))
