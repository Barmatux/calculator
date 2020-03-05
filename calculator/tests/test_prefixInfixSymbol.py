from unittest import TestCase, mock


class TestPrefixInfixSymbol(TestCase):

    @mock.patch('calculator.symbol_classes.Symbol.count', return_value=1)
    def test_nud(self):
        self.fail()


    def test_led(self):
        self.fail()
