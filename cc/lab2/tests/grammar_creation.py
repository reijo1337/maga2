import unittest
from part1.grammar import Grammar
from part1.left_recursion import remove_left_recursion


class GrammarCreationCase(unittest.TestCase):
    def test_grammar_eq(self):
        a = Grammar()
        b = Grammar()
        a.load_from_file('../grammar1')
        b.load_from_file('../grammar1')
        self.assertEqual(a, b)

    def test_grammar_not_eq(self):
        a = Grammar()
        b = Grammar()
        a.load_from_file('../grammar1')
        b.load_from_file('../grammar2')
        self.assertNotEqual(a, b)

    def test_grammar_save(self):
        a = Grammar()
        a.load_from_file('../grammar1')
        a.save_to_file('../saved_grammar1')
        data = [set(open(i).read().split()) for i in ('../grammar1', '../saved_grammar1')]
        self.assertEqual(data[0], data[1])

    def test_grammar_rec_remove(self):
        a = Grammar()
        a.load_from_file('../rec_grammar')
        remove_left_recursion(a)
        a.save_to_file('../non_rec_grammar')
        data = [set(open(i).read().split()) for i in ('../non_rec_grammar', '../non_rec_grammar_check')]
        self.assertEqual(data[0], data[1])


if __name__ == '__main__':
    unittest.main()
