import unittest

from nfa.fa_state import State
from nfa.nfa_builder import build_nfa
from nfa.nfa_to_dfa import e_closure, move, nfa_to_dfa


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = build_nfa('(a|b)*abb')
        a.visualize('test')
        a = build_nfa('(a|b)+abb')
        a.visualize('test_iter')
        self.assertEqual(True, True)

    def test_tool_funcs(self):
        s1 = State('1')
        s2 = State('2')
        s3 = State('3')
        s4 = State('4')
        s1.moveOnChar('a', s2)
        s1.moveOnChar('a', s3)
        s1.moveOnEpsilon(s4)
        self.assertEqual(e_closure({s1}), {s4})
        self.assertEquals(move([s1], 'a'), {s2, s3})

    def test_nfa_to_dfa(self):
        a = build_nfa('(a|b)*abb')
        a.visualize('sas')
        b = nfa_to_dfa(a)
        b.visualize('sas_dfa')


if __name__ == '__main__':
    unittest.main()
