import unittest
from grammar import parse
from part1.grammar import Grammar
from part1.left_recursion import remove_left_recursion


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = Grammar()
        a.load_from_file('grammar')
        remove_left_recursion(a)
        a.save_to_file('new_grammar')
        test_string = 'a & true'
        res = a.check_string(test_string)
        self.assertEqual(True, res)


if __name__ == '__main__':
    unittest.main()
