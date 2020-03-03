import math
from numbers import Number
from operator import *

from error_classes import CalcError

operator_table = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod, '//': floordiv, '^': pow, '<': lt, '<=': le,
                  '==': eq, '>': gt, '>=': ge, '!=': ne, 'abs': abs, 'round': round
                  }
math_const = ['pi', 'e', 'tau', 'inf', 'nan']


class Symbol:
    id = None
    value = 0
    lbp = 0
    token = None
    gen = None

    def __init__(self, id, value, lbp=0):
        self.id = id
        self.value = value
        self.lbp = lbp

    """Base class for symbols in math expression"""

    # def nud(self, token, gen):
    #     raise SyntaxError("Syntax Error {}".format(self))
    #
    # def led(self):
    #     raise SyntaxError("Syntax Error {}".format(self))

    def __repr__(self):
        if self.id == "func" or self.id == "lit":
            return "(%s %s)" % (self.id, self.value)

    @staticmethod
    def expression(rbp=0):
        """ Main function that count result of expression"""
        previous_token = Symbol.token
        Symbol.token = next(Symbol.gen)
        left = previous_token.nud()
        while rbp < Symbol.token.lbp:
            previous_token = Symbol.token
            Symbol.token = next(Symbol.gen)
            if isinstance(left, Number) or left is None:
                left = previous_token.led(left)
            else:
                left = previous_token.led(left.value)
        if isinstance(left, Number):
            return left
        else:
            return left.value


class PostfixSymbol(Symbol):
    def nud(self):
        if self.value in math_const:
            return getattr(math, self.value)
        if self.id == 'func':
            try:
                math_function = getattr(math, self.value)
            except AttributeError:
                raise CalcError('Error no such function')
            else:
                return math_function(self.expression(self.lbp))
        a = self.expression(self.lbp)
        if self.id == '-':
            return -a
        return a


class InfixSymbol(Symbol):
    def led(self, symbol):
        a = self.expression(self.lbp)
        return operator_table[self.id](symbol, a)


class PostfixInfixSymbol(InfixSymbol, PostfixSymbol):
    pass

class Lit(Symbol):
    def nud(self):
        return self.value


class OpenBracket(Symbol):
    def nud(self):
        """ rule for bracket"""
        expr = self.expression()
        self.check_trailing_bracket(")")
        return expr

    def check_trailing_bracket(self, oper_id=None):
        """ Check if we have close bracket, raise exception if no"""
        if oper_id and OpenBracket.token.id != oper_id:
            raise CalcError('unbalanced bracket')
