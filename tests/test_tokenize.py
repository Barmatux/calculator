from unittest import TestCase, mock
from pycalc import tokenize
from const_and_paterns import make_symbol
from symbol_classes import Symbol, Lit


class TestTokenize(TestCase):
    def test_tokenize_lit(self):
        test_list = []
        for i in tokenize(expression='2'):
            test_list.append(i)
        list_of_tokens = [('lit', 2),('end', 0,)]
        self.assertEqual(test_list[0].id, list_of_tokens[0][0])
        self.assertEqual(test_list[0].value, list_of_tokens[0][1])
        self.assertEqual(test_list[1].id, list_of_tokens[1][0])


    def test_tokenize_lit_oper(self):
        test_list =[]
        for i in tokenize(expression='1+2'):
            test_list.append(i)
        list_of_tokens = [('lit', 1,), ('+', 0, 10), ('lit', 2)]
        self.assertEqual(test_list[0].id, list_of_tokens[0][0])
        self.assertEqual(test_list[0].value, list_of_tokens[0][1])
        self.assertEqual(test_list[1].id, list_of_tokens[1][0])
        self.assertEqual(test_list[1].lbp, list_of_tokens[1][1])
        self.assertEqual(test_list[2].id, list_of_tokens[2][0])
        self.assertEqual(test_list[2].value, list_of_tokens[2][1])


    def test_tokenize_lit_func(self):
        test_list = []
        for i in tokenize(expression='cos(e)'):
            test_list.append(i)
        list_of_tokens = [('func', 'cos', 200), ('(', 0, 150), ('func', 'e'), (')', 0, 0)]
        self.assertEqual(test_list[0].id, list_of_tokens[0][0])
        self.assertEqual(test_list[0].value, list_of_tokens[0][1])
        self.assertEqual(test_list[0].lbp, list_of_tokens[0][2])
        self.assertEqual(test_list[1].id, list_of_tokens[1][0])
        self.assertEqual(test_list[1].lbp, list_of_tokens[1][2])
        self.assertEqual(test_list[2].id, list_of_tokens[2][0])
        self.assertEqual(test_list[2].value, list_of_tokens[2][1])
        self.assertEqual(test_list[3].id, list_of_tokens[3][0])
        self.assertEqual(test_list[3].lbp, list_of_tokens[3][2])