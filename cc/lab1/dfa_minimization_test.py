import unittest
from fa_state import State
from fa import Automata
from fa_minimization import minimize, minimization
import syntax_tree as st


class MyTestCase(unittest.TestCase):
    def test_minimization(self):
        start_dfa = build_dfa()
        start_dfa.visualize('start.gv')
        min_dfa = minimize(start_dfa)
        min_dfa.visualize('min.gv')
        self.assertEqual(True, True)

    def test_tree_build(self):
        regex = '(a(b|a))+b'
        tree = st.build_tree(regex)
        st.visualize_tree(tree, regex)
        self.assertEqual(True, True)

    def test_minimize(self):
        origin_dfa = build_minimize_dfa()
        origin_dfa.visualize('origin')
        min_dfa = minimization(origin_dfa)
        min_dfa.visualize('min')
        self.assertEqual(True, True)


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


def build_minimize_dfa():
    states = list()
    for i in range(7):
        states.append(State(positions={i+1}))
    states[0].moveOnChar('a', states[6])
    states[0].moveOnChar('b', states[1])
    states[1].moveOnChar('a', states[6])
    states[1].moveOnChar('b', states[0])
    states[2].moveOnChar('a', states[3])
    states[2].moveOnChar('b', states[4])
    states[3].moveOnChar('a', states[4])
    states[3].moveOnChar('b', states[5])
    states[4].moveOnChar('a', states[4])
    states[4].moveOnChar('b', states[4])
    states[5].moveOnChar('a', states[5])
    states[5].moveOnChar('b', states[4])
    states[6].moveOnChar('a', states[2])
    states[6].moveOnChar('b', states[2])
    states[4].isFinalState = True
    states[5].isFinalState = True
    return Automata(startState=states[0])