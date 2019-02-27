from fa_state import State
from graphviz import Digraph


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

    def visualize(self):
        """
        Визуализация ДКА с помощью graphviz
        """
        fa_graph = Digraph('finite_state_machine', filename='fa.gv')
        self.___visualize_final_states__(fa_graph, self.startState)
        fa_graph.attr('node', shape='circle')
        fa_graph.edge('START', str(self.startState))
        self.__visualize_state__(fa_graph, self.startState)
        fa_graph.view()

    def __visualize_state__(self, graph, state):
        """
        Добавление в визуализацию состояния и всех переходов из него
        :type state: State
        :type graph: Digraph
        """
        for char_transition in state.charTransitions:
            if len(char_transition) != 0:
                code = state.charTransitions.index(char_transition)
                for dest_state in char_transition:
                    graph.edge(str(state), str(dest_state), label=chr(code))
                    self.__visualize_state__(graph, dest_state)

    def ___visualize_final_states__(self, graph, state):
        graph.attr('node', shape='doublecircle')
        if state.isFinalState:
            graph.node(str(state))
        for char_transition in state.charTransitions:
            if len(char_transition) != 0:
                for dest_state in char_transition:
                    self.___visualize_final_states__(graph, dest_state)
