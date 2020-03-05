from unittest import TestCase, mock
from operator import mul
from calculator.symbol_classes import InfixSymbol

from calculator.symbol_classes import InfixSymbol


class TestInfixSymbol(TestCase):




    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=1)
    def test_led_mul(self, symbol):
        symbol = 2
        c = InfixSymbol('*', 0, 20)
        self.assertEqual(c.led(symbol), 2)

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=2)
    def test_led_div(self, symbol):
        symbol = 4
        c = InfixSymbol('/', 0, 20)
        self.assertEqual(c.led(symbol), 2)

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=1)
    def test_led_comparison_lt(self, symbol):
        symbol = 2
        c = InfixSymbol('>', 0, 20)
        self.assertTrue(c.led(symbol))

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=1)
    def test_led_comparison_eq(self, symbol):
        symbol = 2
        c = InfixSymbol('==', 0, 20)
        self.assertFalse(c.led(symbol))