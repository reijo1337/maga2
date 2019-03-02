import unittest
from fa_state import State
from fa import Automata
from fa_minimization import minimize


class MyTestCase(unittest.TestCase):
    def test_something(self):
        start_dfa = build_dfa()
        start_dfa.visualize('start.gv')
        min_dfa = minimize(start_dfa)
        min_dfa.visualize('min.gv')
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()


def build_dfa():
    states = list()
    for i in range(5):
        states.append(State(positions={i+1}))
    states[0].moveOnChar('a', states[2])
    states[0].moveOnChar('b', states[1])
    states[1].moveOnChar('b', states[0])
    states[1].moveOnChar('a', states[3])
    states[2].moveOnChar('b', states[3])
    states[2].moveOnChar('a', states[4])
    states[3].moveOnChar('a', states[3])
    states[3].moveOnChar('b', states[3])
    states[4].moveOnChar('a', states[2])
    states[4].moveOnChar('b', states[1])
    states[0].isFinalState = True
    states[4].isFinalState = True
    dfa = Automata(startState=states[0])
    return dfa