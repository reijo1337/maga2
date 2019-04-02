import unittest

from part1.grammar import Grammar
from part2.eps_remove import eps_rules_finder


class MyTestCase(unittest.TestCase):
    def test_eps_finder(self):
        a = Grammar()
        a.load_from_file('../check_eps_finder')
        non_terminals = eps_rules_finder(a)
        non_terminals_check = {'A', 'B', 'C', 'S'}
        self.assertEqual(non_terminals, non_terminals_check)


if __name__ == '__main__':
    unittest.main()
