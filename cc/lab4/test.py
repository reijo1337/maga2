import unittest
from operator_precedence import main


class MyTestCase(unittest.TestCase):
    def test_ok(self):
        input_string = 'a ! ~ a & f'
        self.assertEqual(0, main(input_string))
        input_string = 't ! ~ f & a'
        self.assertEqual(0, main(input_string))

    def test_ok_double_not(self):
        input_string = 'a ! ~ ~ a & f'
        self.assertEqual(0, main(input_string))

    def test_not_ok_1(self):
        input_string = 'a ! ~ ! a & f'
        self.assertEqual(1, main(input_string))
        input_string = 'a ! ! a & f'
        self.assertEqual(1, main(input_string))
        input_string = 'a ! & a & f'
        self.assertEqual(1, main(input_string))
        input_string = 'a & & a & f'
        self.assertEqual(1, main(input_string))

    def test_not_ok_2(self):
        input_string = 'a ! ~ a a & f'
        self.assertEqual(2, main(input_string))
        input_string = 'a ! t a & f'
        self.assertEqual(2, main(input_string))
        input_string = 'a ! f a & f'
        self.assertEqual(2, main(input_string))
        input_string = 'a & f f & f'
        self.assertEqual(2, main(input_string))

    def test_not_ok_3(self):
        input_string = 'a ! a ~ a & f'
        self.assertEqual(3, main(input_string))


if __name__ == '__main__':
    unittest.main()
