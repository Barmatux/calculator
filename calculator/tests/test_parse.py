from unittest import TestCase
from calculator.pycalc import parse
from math import cos, log10, pi, e, sin
from calculator.symbol_classes import *

class TestParse(TestCase):
    def setUp(self) -> None:
        symbol_table = {
            "+": PostfixInfixSymbol("+", 0, 10),
            "-": PostfixInfixSymbol("-", 0, 10),
            "*": InfixSymbol("*", 0, 20),
            "/": InfixSymbol("/", 0, 20),
            "//": InfixSymbol("//", 0, 2),
            "%": InfixSymbol("%", 0, 20),
            "^": InfixSymbol("^", 0, 30),
            "<": InfixSymbol("<", 0, 5),
            "<=": InfixSymbol("<=", 0, 5),
            ">": InfixSymbol(">", 0, 5),
            ">=": InfixSymbol(">=", 0, 5),
            "!=": InfixSymbol("!=", 0, 5),
            "==": InfixSymbol("==", 0, 5),
            "lit": Lit("lit", 0),
            "end": Lit("end", 0),
            ",": Lit(",", 0),
            ")": Lit(")", 0),
            "(": OpenBracket("(", 0, 150),
            "func": PostfixSymbol('func', 0, 200)
        }

    def TearDown(self):
        exit()


    def test_parse_unary_brackets(self):
        res = parse(inpt='6-(-13)')
        self.assertEqual(res, 6-(-13))

    def test_parse_unary_multi_opeators(self):
        res = parse(inpt='--+2')
        self.assertEqual(res, --+2)

    def test_parse_unary_multi_opeators_neg(self):
        res = parse(inpt='--+-2')
        self.assertEqual(res, --+-2)

    def test_parse_unary_sub(self):
        res = parse(inpt='-2--+2')
        self.assertEqual(res, -2--+2)

    def test_parse_priority_mul(self):
        res = parse(inpt='2+2*3')
        self.assertEqual(res, 2+2*3)

    def test_parse_priority_mul_neg(self):
        res = parse(inpt='2-2*3')
        self.assertEqual(res, 2-2*3)

    def test_parse_priority_mul_bracket(self):
        res = parse(inpt='2+(2+2*2)-3')
        self.assertEqual(res, 2+(2+2*2)-3)

    def test_parse_priority_pow(self):
        res = parse(inpt='2*3^2')
        self.assertEqual(res, 18)

    def test_parse_priority_all(self):
        res = parse(inpt='100/2^2*2')
        self.assertEqual(res, 100/2**2*2)

    def test_parse_priority_multi_pow(self):
        res = parse(inpt='2^2^3')
        self.assertEqual(res, 64)

    def test_parse_priority_assot(self):
        res = parse(inpt='100/4/3')
        self.assertEqual(res, 100/4/3)

    def test_comparison_operators(self):
        res = parse(inpt='3>2')
        self.assertTrue(res)

    def test_parse_comparison_operators_eq1(self):
        res = parse(inpt='3==2')
        self.assertFalse(res)

    def test_parse_comparison_operators_eq2(self):
        res = parse(inpt='3==3')
        self.assertTrue(res)

    def test_parse_comparison_operators_not_eq(self):
        res = parse(inpt='5!=3')
        self.assertTrue(res)

    def test_parse_comparison_operators_not_le(self):
        res = parse(inpt='5>=5')
        self.assertTrue(res)

    def test_parse_func_abs(self):
        res = parse(inpt='abs(-2)')
        self.assertEqual(res, 2)

    def test_parse_func_cos(self):
        res = parse(inpt='cos(0.5)')
        self.assertEqual(res, cos(0.5))

    def test_parse_func_log(self):
        res = parse(inpt='log10(100)')
        self.assertEqual(res, log10(100))

    def test_parse_func_const(self):
        res = parse(inpt='2*pi')
        self.assertEqual(res, 2*pi)

    def test_parse_common1(self):
        res = parse(inpt='2.0^(pi/pi+e/e+2.0^0.0)')
        self.assertEqual(res, 2.0**(pi/pi+e/e+2.0**0.0))

    def test_parse_common2(self):
        res = parse(inpt='sin(pi/2^1)')
        self.assertEqual(res, sin(pi/2**1))

    def test_parse_common3(self):
        res = parse(inpt='3+2*2-3/3')
        self.assertEqual(res, 3+2*2-3/3)

    def test_parse_priority_power(self):
        res = parse(inpt='-2^2')
        self.assertEqual(res, -2^2)

    def test_parse_priority_power1(self):
        res = parse(inpt='-2-(-2*2)')
        self.assertEqual(res, -2-(-2*2))

    def test_parse_unar(self):
        res = parse(inpt='-2+--3')
        self.assertEqual(res, (-2+--3))

    def test_parse_comm(self):
        res = parse(inpt='cos(-1)+1')
        self.assertEqual(res, cos(-1)+1)
