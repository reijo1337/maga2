import unittest
from part1.grammar import Grammar
from part1.left_recursion import remove_left_recursion
from part2.eps_remove import eps_remove


class MyTestCase(unittest.TestCase):
    def test_wrong(self):
        a = Grammar()
        a.load_from_file('grammar')
        remove_left_recursion(a)
        a = eps_remove(a)
        a.save_to_file('new_grammar')
        test_string = 'a = a ! ~ сосать a & false'
        res = a.check_string(test_string)
        self.assertEqual(False, res)

    def test_ok(self):
        a = Grammar()
        a.load_from_file('grammar')
        remove_left_recursion(a)
        a = eps_remove(a)
        a.save_to_file('new_grammar')
        test_string = 'a = a ! ~ a & false'
        res = a.check_string(test_string)
        self.assertEqual(True, res)


if __name__ == '__main__':
    unittest.main()
