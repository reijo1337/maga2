import syntax_tree as st
from fa_state import State
from fa import Automata


def build_for_regexp(regexp):
    """
    Построение ДКА из регуляьрного выражения
    :type regexp: str
    """
    Q = {
        'marked': list(),
        'unmarked': list(),
    }
    char_position = dict()
    for char in regexp:
        char_position.setdefault(char, list())

    # Построить синтаксическое дерево для пополненного регулярного выражения (r)#
    tree = st.build_tree(regexp)
    # Обходя синтаксическое дерево, вычислить значения функций nullable, firstpos, lastpos и followpos.
    followpos_dict = st.get_followpos(tree)
    # Определить q0 = firstpos(root), где root - корень синтаксического дерева.
    q0 = State(positions=st.firstpos(tree))
    # Добавить q0 в Q как непомеченное состояние
    Q['unmarked'].append(q0)

    for key in char_position.keys():
        char_position[key] = st.get_char_positions(tree, key)

    # while (в Q есть непомеченное состояние R)
    while len(Q['unmarked']) != 0:
        # пометить R
        R: State = Q['unmarked'].pop(0)
        Q['marked'].append(R)

        # for (каждого входного символа a  T , такого, что в R имеется позиция, которой соответствует a)
        for char in char_position.keys():
            p: set = R.positions.intersetion(set(char_position[char]))
            # пусть символ a в R соответствует позициям p1, ..., pn
            if len(p) != 0:
                # и пусть S =  1<i<n followpos(pi)
                S_set = set()
                for pi in p:
                    S_set.update(followpos_dict[pi])
                # if (S)
                if len(S_set) != 0:
                    S = State(positions=S_set)
                    # if (SQ)
                    if S not in Q['marked'] and S not in Q['unmarked']:
                        # добавить S в Q как непомеченное состояние
                        Q['unmarked'].append(S)
                    # определить D(R, a) = S;
                    R.moveOnChar(character=char, destinationState=S)

    # Определить F как множество всех состояний из Q, содержащих позиции, связанные с символом #
    end_key_position = max(followpos_dict.keys())
    for state in Q['marked']:
        if end_key_position in state.positions:
            state.isFinalState = True

    return Automata(q0)
