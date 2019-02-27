from fa_state import State


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
