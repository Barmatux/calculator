import math
from numbers import Number
from operator import *

from calculator.error_classes import CalcError

operator_table = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod, '//': floordiv, '^': pow, '<': lt, '<=': le,
                  '==': eq, '>': gt, '>=': ge, '!=': ne, 'abs': abs, 'round': round,
                  }
math_const = ['pi', 'e', 'tau', 'inf', 'nan']


class Symbol:
    current_token = None
    all_tokens = None
    tk_power = 0

    def __init__(self, id, value, token_power=0, counter=0):
        self.id = id
        self.value = value
        self.token_power = token_power
        self.counter = counter

    """Base class for symbols in math expression"""

    def nud(self):
        raise SyntaxError("Syntax Error {}".format(self))

    def led(self, symbol):
        raise SyntaxError("Syntax Error {}".format(self))

    def __repr__(self):
        return "(%s %s)" % (self.id, self.value)

    def count(self):
        """ Main function that count result of expression"""
        previous_token = Symbol.current_token
        try:
            Symbol.current_token = next(Symbol.all_tokens)
        except StopIteration as e:
            raise CalcError('Error: wrong expression')
        left = previous_token.nud()
        Symbol.tk_power = Symbol.count_token_power(self)
        while self.token_power < Symbol.tk_power:
            previous_token = Symbol.current_token
            Symbol.current_token = next(Symbol.all_tokens)
            Symbol.tk_power = Symbol.count_token_power(self)
            if isinstance(left, Number) or left is None:
                left = previous_token.led(left)
            else:
                left = previous_token.led(left.value)
        if isinstance(left, Number):
            return left
        else:
            return left.value

    def count_token_power(self):
        if self.current_token.id != '^':
            return self.current_token.token_power
        else:
            return self.current_token.token_power + 1


class PrefixSymbol(Symbol):
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


class PrefixInfixSymbol(InfixSymbol, PrefixSymbol):
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
    """ Literal class which ovveride method nud, return itself value"""
    def nud(self):
        return self.value


class OpenBracket(Symbol):
    def nud(self):
        """ Special class for open bracket, begin new calculation with high priority"""
        self.token_power = 0
        expr = self.count()
        self.check_trailing_bracket(")")
        return expr

    def check_trailing_bracket(self, oper_id=None):
        """ Check if we have close bracket, raise exception if no"""
        if oper_id and OpenBracket.current_token.id != oper_id:
            raise CalcError('Error: unbalanced bracket')
        Symbol.current_token = next(Symbol.all_tokens)
