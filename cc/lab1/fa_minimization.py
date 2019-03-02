from typing import Any, Union, List

from fa import Automata
from fa_state import State
import numpy as np
from disjoint_set import DisjointSet

alph = "abcdefghijklmnopqrstuvwxyz"


def build_table(states, sigma_minus_one):
    n = len(states)
    Q = list()
    marked = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if not marked[i][j] and states[i].isFinalState != states[j].isFinalState:
                marked[i][j] = marked[j][i] = True
                Q.append((i, j))

    print(marked)

    while len(Q) != 0:
        u, v = Q.pop(0)
        for c in alph:
            for r in [j for j, val in enumerate(sigma_minus_one[u]) if val == c]:
                for s in [j for j, val in enumerate(sigma_minus_one[v]) if val == c]:
                    if not marked[r][s]:
                        marked[r][s] = marked[s][r] = True
                        Q.append((r, s))
    return marked


def minimization(dfa):
    """
	Минимизация ДКА
	:type dfa: Automata
	"""
    states = dfa.states()
    sigma_minus_one = dfa.reverseEdgesTable()
    print(sigma_minus_one)
    states.insert(0, State(positions={0}))
    states_str = ''
    for state in states:
        states_str = states_str + str(state) + ' '
    print(f'States: {states_str}')

    marked = build_table(states, sigma_minus_one)
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
    print(component)


def minimize(dfa):
    """
	Минимизация ДКА
	:type dfa: Automata
	"""

    global state, start_state

    def order_tuple(a, b):
        """
        :type b: State
        :type a: State
        """
        return (a, b) if list(a.positions) < list(b.positions) else (b, a)

    table = {}

    def state_key(state):
        return list(state.positions)

    sorted_states = sorted(dfa.states(), key=state_key)
    final_states = list()

    for state in sorted_states:
        if state.isFinalState:
            final_states.append(state)
    for i, item in enumerate(sorted_states):
        for item_2 in sorted_states[i + 1:]:
            table[(item, item_2)] = (item in final_states) != (item_2 in final_states)

    flag = True
    # table filling method
    while flag:
        flag = False

        for i, item in enumerate(sorted_states):
            for item_2 in sorted_states[i + 1:]:

                if table[(item, item_2)]:
                    continue

                # check if the states are distinguishable
                for w in alph:
                    t1_list = item.charTransitions[ord(w)]
                    t2_list = item_2.charTransitions[ord(w)]

                    if t1_list is not None and t2_list is not None and t1_list != t2_list:
                        marked = table[order_tuple(t1_list, t2_list)]
                        flag = flag or marked
                        table[(item, item_2)] = marked

                        if marked:
                            break

    d = DisjointSet(dfa.states())
    for k, v in table.items():
        if not v:
            d.union(k[0], k[1])
    states = []
    orig_states = dfa.states()
    start_state = State({0})
    # Строим новые состояния КА
    for set_states in d.get():
        f = False
        for al in states:
            if al.positions == d.find_set(set_states[0]):
                state = al
                f = True
                break
        if not f:
            state = State(d.find_set(set_states[0]))
            states.append(state)
        # Если получили начальное состояние
        if dfa.startState in set_states:
            start_state = state
        # Если получили конечное состояние
        for item in set_states:
            if item in final_states:
                state.isFinalState = True
                break
        # Перенос переходов
        for item in set_states:
            for orig_state in orig_states:
                # Нашли состояние, которое легло в основу нового
                if item == orig_state:
                    # Перенос переходов со старого состояния на новое
                    for char_code, orig_dest_states in enumerate(orig_state.charTransitions):
                        if orig_dest_states is not None:
                            # Находим новое состояние, в которое нужно построить переход
                            finded = False
                            for new_state in states:
                                if orig_dest_states.positions in new_state.positions:
                                    state.moveOnChar(chr(char_code), new_state)
                                    finded = True
                            # Если нового состояния еще нет, то надо его создать
                            if not finded:
                                dest_state = State(d.find_set(orig_dest_states))
                                state.moveOnChar(chr(char_code), dest_state)
                                states.append(dest_state)
    return Automata(startState=start_state)
