from fa import Automata
from fa_state import State
import numpy as np


def build_table(states, sigma_minus_one, alph):
    n = len(states)
    Q = list()
    marked = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if not marked[i][j] and states[i].isFinalState != states[j].isFinalState:
                marked[i][j] = True
                marked[j][i] = True
                Q.append((i, j))
    print('Инициализировали таблицу:')
    print(marked)
    while len(Q) != 0:
        u, v = Q.pop(0)
        for c in alph:
            for s in [k for k, vall in enumerate(sigma_minus_one[v]) if c in vall.decode('utf-8')]:
                for r in [j for j, val in enumerate(sigma_minus_one[u]) if c in val.decode('utf-8')]:
                    if not marked[r][s]:
                        # for ii in range(s+1):
                        #     if ii < r:
                        #         marked[r][ii] = True
                        #         marked[ii][r] = True
                        marked[r][s] = marked[s][r] = True
                        Q.append((r, s))
    for i in range(1, n):
        marked[0][i] = True
        marked[i][0] = True
    return marked


def minimization(dfa):
    """
	Минимизация ДКА
	:type dfa: Automata
	"""
    alph = dfa.alphabet()
    states = dfa.states()
    sigma_minus_one = dfa.reverse_edges_table()
    print('Таблица обратных переходов:')
    print(sigma_minus_one)
    states.insert(0, State(positions={0}))
    states_str = ''
    for state in states:
        states_str = states_str + str(state) + ' '
    print(f'States: {states_str}')

    marked = build_table(states, sigma_minus_one, alph)
    print('Вычислили таблицу:')
    print(marked)
    component = [-1 for _ in states]
    for i, _ in enumerate(states):
        if not marked[0][i]:
            component[i] = 0

    components_count = 0
    for i in range(1, len(states)):
        if component[i] == -1:
            components_count = components_count + 1
            component[i] = components_count
            for j in range(i + 1, len(states)):
                if not marked[i][j]:
                    component[j] = components_count
    print('Группировка')
    print(component)
    return build_min_dfa(component, states, dfa.startState)


def build_min_dfa(component, states, start_state):
    """
    Построение нового минимизированного ДКА
    :param start_state: State
    :param component: list
    :type states: list
    """
    global start
    count_of_states = max(component)
    groups = [State({i}) for i in range(count_of_states)]
    component.pop(0)
    states.pop(0)
    for i, state in enumerate(states):
        new_state_index = component[i] - 1
        new_state = groups[new_state_index]
        if state.isFinalState:
            new_state.isFinalState = True
        if state == start_state:
            start = new_state
        for code, dest in enumerate(state.charTransitions):
            if dest is not None and dest.positions != {0}:
                j = states.index(dest)
                new_dest_index = component[j] - 1
                new_dest = groups[new_dest_index]
                new_state.moveOnChar(chr(code), new_dest)

    return Automata(start)
