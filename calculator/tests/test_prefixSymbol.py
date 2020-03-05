from unittest import TestCase, mock
from calculator.symbol_classes import PrefixSymbol
import math


class TestPrefixSymbol(TestCase):

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=5)
    def test_nud_cos(self, mock):
        c = PrefixSymbol('func', 'cos', 20)
        self.assertEqual(c.nud(), math.cos(5))

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=0)
    def test_nud_constant(self, mock):
        c = PrefixSymbol('func', 'e', 20)
        self.assertEqual(c.nud(), math.e)

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=-2)
    def test_nud_abs(self, mock):
        c = PrefixSymbol('func', 'abs', 20)
        self.assertEqual(c.nud(), 2)


    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=-2)
    def test_nud_sin_negative(self, mock):
        c = PrefixSymbol('func', 'sin', 20)
        self.assertEqual(c.nud(), math.sin(-2))