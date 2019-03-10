from fa_state import State
from graphviz import Digraph
import numpy as np


class Automata(object):
    """Represents the Non-deterministic Finite Automata."""

    def __init__(self, startState):
        """
		Initialise the NFA with start and terminating state.
		Params:
			startState: starting state of the NFA
			endState: ending state of the NFA
		"""

        if not isinstance(startState, State):
            raise ValueError("Invalid parameters passed")

        self.startState = startState

    def matches(self, string):
        """
		Check if string can be simulated successfully from the start state.
		Params:
			string - input for which pattern matching is performed
		"""

        return self.startState and self.startState.matches(string)

    def visualize(self, filename):
        """
        Визуализация ДКА с помощью graphviz
        """
        fa_graph = Digraph('finite_state_machine')
        states = self.states()
        fa_graph.attr('node', shape='doublecircle')
        for state in states:
            if state.isFinalState:
                fa_graph.node(str(state))
        fa_graph.attr('node', shape='circle')
        fa_graph.edge('START', str(self.startState))
        for state in states:
            for code, char_transition in enumerate(state.charTransitions):
                if char_transition is not None:
                    # code = state.charTransitions.index(char_transition)
                    fa_graph.edge(str(state), str(char_transition), label=chr(code))
        fa_graph.view(filename=filename)

    def states(self):
        """
        Возвращает список состояний автомата
        :return: список состояний
        """
        visited = list()
        state_stack = list()
        state_stack.append(self.startState)
        while len(state_stack) != 0:
            state = state_stack.pop(len(state_stack) - 1)
            if state not in visited:
                visited.append(state)
                for destinations in state.charTransitions:
                    if destinations is not None and destinations not in visited:
                        state_stack.append(destinations)
        return visited

    def reverseEdgesTable(self):
        states = self.states()
        alph = "abcdefghijklmnopqrstuvwxyz"
        size = len(states)
        # Таблица переходов. Строка - входное состояние, столбец - выходное
        sigma = np.zeros((size+1, size+1), dtype=str)
        for num, state in enumerate(states):
            for code, destiantions in enumerate(state.charTransitions):
                if len(destiantions) != 0:
                    if chr(code) in alph:
                        alph = alph.replace(chr(code), '')
                    for dest in destiantions:
                        dest_index = states.index(dest)
                        sigma[dest_index+1][num+1] = chr(code)
        for i in range(1, size + 1):
            sigma[0][i] = alph
        return sigma

    def check(self, check_string):
        """
        Проверка строки на соответсвие исходному регулярному выражению
        :type check_string: str
        """
        print(f'Исходная строка: {check_string}')
        current_state = self.startState
        for c in check_string:
            next_state = current_state.getTransitionsForChar(c)
            if next_state is not None:
                print(f'Текущее состояние: {str(current_state)}. Переход по букве {c} в состояние {str(next_state)}')
                current_state = next_state
            else:
                print(f'Текущее состояние: {str(current_state)}. Переход по букве {c} невозможен')
                break
        if current_state.isFinalState:
            print(f'Автомат пришел в конечное состояние {str(current_state)}. Строка подходит')
        else:
            print(f'Автомат пришел в не конечное состояние {str(current_state)}. Строка не подходит')
