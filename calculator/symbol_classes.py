import math
from numbers import Number
from operator import *

from calculator.error_classes import CalcError

operator_table = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod, '//': floordiv, '^': pow, '<': lt, '<=': le,
                  '==': eq, '>': gt, '>=': ge, '!=': ne, 'abs': abs, 'round': round
                  }
math_const = ['pi', 'e', 'tau', 'inf', 'nan']


class Symbol:
    current_token = None
    all_tokens = None

    def __init__(self, id, value, token_power=0):
        self.id = id
        self.value = value
        self.token_power = token_power

    """Base class for symbols in math expression"""

    def nud(self):
        raise SyntaxError("Syntax Error {}".format(self))

    def led(self):
        raise SyntaxError("Syntax Error {}".format(self))

    def __repr__(self):
        if self.id == "func" or self.id == "lit":
            return "(%s %s)" % (self.id, self.value)

    def count(self):
        """ Main function that count result of expression"""
        previous_token = Symbol.current_token
        Symbol.current_token = next(Symbol.all_tokens)
        left = previous_token.nud()
        while self.token_power < Symbol.current_token.token_power:
            previous_token = Symbol.current_token
            Symbol.current_token = next(Symbol.all_tokens)
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
        if self.value in operator_table:
            counted_value = operator_table[self.value](self.count())
            self.token_power = 0
            return counted_value
        if self.value in math_const:
            counted_val = getattr(math, self.value)
            self.token_power = 0
            return counted_val
        if self.id == 'func':
            try:
                math_function = getattr(math, self.value)
            except AttributeError:
                raise CalcError('Error no such function')
            else:
                counted_val = math_function(self.count())
                self.token_power = 0
                return counted_val



class InfixSymbol(Symbol):
    def led(self, symbol):
        a = self.count()
        return operator_table[self.id](symbol, a)


class PostfixInfixSymbol(InfixSymbol, PostfixSymbol):
    def nud(self):
        self.token_power = 100
        a = self.count()
        self.token_power = 0
        if self.id == '-':
            return -a
        return a

    def led(self, symbol):
        self.token_power = 10
        a = self.count()
        return operator_table[self.id](symbol, a)


class Lit(Symbol):
    def nud(self):
        return self.value


class OpenBracket(Symbol):
    def nud(self):
        """ rule for bracket"""
        self.token_power = 0
        expr = self.count()
        self.check_trailing_bracket(")")

        return expr

    def check_trailing_bracket(self, oper_id=None):
        """ Check if we have close bracket, raise exception if no"""
        if oper_id and OpenBracket.current_token.id != oper_id:
            raise CalcError('Error: unbalanced bracket')
        Symbol.current_token = next(Symbol.all_tokens)
