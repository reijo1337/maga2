class State(object):
    """Represents the state/node in a Non-deterministic Finite Automata."""

    def __init__(self, positions, isFinalState=False):
        """
        Initialise the state type and transition arrays.
        Params:
            isFinalState: True if this is final state state, False otherwise
        """

        self.charRangeMin = 97
        self._charRangeMax = 122

        self.positions = positions
        self.isFinalState = isFinalState
        self.charTransitions = {code: list() for code in range(self.charRangeMin, self._charRangeMax)}
        self.epsilonTransitions = list()

    def __str__(self):
        return str(self.positions)

    def isSupportedChar(self, character):
        """
        Check if input character is in valid ASCII range.
        Params:
            character - input symbol
        Returns:
            True if input is an ascii symbol is in supported range, else False
        """

        if len(character) > 1:
            raise ValueError("Expected a empty or one character string")

        if len(character) == 0:
            return True

        return self.charRangeMin <= ord(character) <= self._charRangeMax

    def moveOnChar(self, character, destinationState):
        """
        Add a character transition to destinationState.
        Params:
            character - symbol for which this transition is defined
            destinationState - state to which transition leads to
        """

        if not (isinstance(character, str)
                and isinstance(destinationState, State)):
            raise ValueError("Invalid parameters passed")

        if not self.isSupportedChar(character):
            raise ValueError(f'Character symbol is invalid: {character}')

        charAsciiValue = ord(character)
        self.charTransitions[charAsciiValue].append(destinationState)

    def moveOnEpsilon(self, destinationState):
        """
        Add an empty move from this state to next.
        Params:
            destinationState - state to which transition leads to
        """

        if not isinstance(destinationState, State):
            raise ValueError("Invalid parameters passed")

        self.epsilonTransitions.append(destinationState)

    def matches(self, string):
        """
        Matches string against pattern represented by the NFA.
        Params:
            string - input for which pattern matching is performed
        Returns:
            True if string matches pattern (NFA), False otherwise
        """
        return self.simulateNfa(string)

    def simulateNfa(self, string):
        """
        Simulate NFA one character at a time from the string.
        Params:
            string: input string to be matched against the NFA for regex
        Returns:
            Boolean: True if match is successful, false otherwise
        """
        epsMoves = self.getEpsReachability()

        for ch in string:
            charMoves = set()
            for state in epsMoves:
                if state.isFinalState:
                    continue
                for move in state.getTransitionsForChar(ch):
                    charMoves.add(move)

            epsMoves = self.getEpsReachabilityForStates(charMoves)

        for state in epsMoves:
            if state.isFinalState:
                return True

        return False

    def getTransitionsForChar(self, ch):
        """
        Get character transitions from this state using ch
        Params:
            ch - character for which transitions are to be retrieved
        Returns:
            list of character transitions from this state using ch
        """
        if not self.isSupportedChar(ch): return []
        return self.charTransitions[ord(ch)]

    def getEpsReachability(self, visited=None):
        """
        Searching epsilon reachable states from self.
        Params:
            visited - set of visited states
        Returns:
            set of epsilon reachable states from self
        """
        stack = [self, ]
        if visited is None: visited = set()
        skip = True

        while stack:
            curr = stack.pop()

            if curr not in visited:
                # In the beginning, we don't include the state itself, however it
                # maybe reachable by kleene loop
                # if not skip:
                visited.add(curr)
                # skip = False
                stack.extend([state for state in curr.epsilonTransitions if state not in visited])

        return visited

    @staticmethod
    def getEpsReachabilityForStates(sources, visited=None):
        """
        Searching epsilon reachable states from multiple sources.
        Params:
            sources - states from which epsilon transitions start
            visited - set of visited states
        Returns:
            set of epsilon reachable states from source states
        """
        if visited is None: visited = set()

        for state in sources:
            if state not in visited:
                state.getEpsReachability(visited)

        return visited

    def simulateNfaBacktrack(self, string, processedStates):
        """
        Simulate NFA one character at a time from the string.
        Params:
            string - input for which pattern matching is performed
            processedStates - set of states that were matched partial pattern
        Returns:
            True if the NFA reaches the final state, False otherwise
        """

        # If loop exists in NFA, return False
        if self in processedStates: return False

        processedStates.add(self)

        if string:
            # If string is non-empty, check if the substring from second
            # character (if any) can be processed by the NFA starting with
            # the character transitions of the first character
            firstChar = string[0]

            if self.isSupportedChar(firstChar):
                for nextState in self.charTransitions[ord(firstChar)]:
                    if nextState.matches(string[1:]): return True

            # or, if still there is no match found, try repeating the process
            # from next node by making an epsilon move

            for epsilonState in self.epsilonTransitions:
                if epsilonState.simulateNfa(string, processedStates): return True

        else:
            # If string has been completely processed, check if we're in
            # final state. If yes, the string matched correctly
            if self.isFinalState: return True

            # otherwise go to neighbors using epsilon moves, and try to
            # reach the final state
            for epsilonState in self.epsilonTransitions:
                if epsilonState.simulateNfa('', processedStates): return True

        return False
