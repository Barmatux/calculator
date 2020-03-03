import re
from operator import add, sub, mul, truediv, mod, le, lt, eq
from numbers import Number
import math

global token, gen


def expression(rbp=0):
    global token
    t = token
    token = next(gen)
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(gen)
        left = t.led(left)
    return left


class symbol_base:
    id=None
    value=None

    def nud(self):
        raise SyntaxError("Syntax error (%r)." % self.id)

    def led(self):
        raise SyntaxError("Syntax error (%r)." % self.id)

    def __repr__(self):
        if self.id == "(name)" or self.id == "(literal)":
            return "(%s %s)" % (self.id[1:-1], self.value)
        out = [self.id]
        out = map(str, filter(None, out))
        return "(" + " ".join(out) + ")"


symbol_table = {}

operator_table = {'+': add, '-': sub, '*': mul, '/': truediv, '%': mod, '^' : pow, '>': lt, '<': le, '=': eq}


def symbol(id, bp=0):
    try:
        s = symbol_table[id]
    except KeyError:
        class s(symbol_base):
            pass
        s.id = id
        s.lbp = bp
        symbol_table[id] = s
    else:
        s.lbp = max(bp, s.lbp)
    return s


def infix(id, bp):
    def led(self, left):
        a = expression(bp)
        if isinstance(a, Number) and isinstance(left, Number):
            symbol = symbol_table['(literal)']
            s = symbol()
            s.value = left
            k = symbol()
            k.value = a
            return operator_table[id](float(s.value), float(k.value))
        elif isinstance(left, Number):
            return operator_table[id](float(left), float(a.value))
        elif isinstance(a, Number):
            symbol = symbol_table['(literal)']
            s = symbol()
            s.value = a
            return operator_table[id](float(left.value), float(s.value))
        else:
            return operator_table[id](float(left.value), float(a.value))
    symbol(id, bp).led = led


def prefix(id, bp):
    def nud(self):
        if self.id == 'func':
            x = getattr(math, self.value)
            return x(float(expression(bp).value))
        a = expression(bp)
        if not isinstance(a, float):
            a = float(a.value)
        if id == '+':
            return a
        elif id == '-':
            return -a
    symbol(id).nud = nud


def nud(self):
    expr = expression()
    advance(")")
    return expr
symbol("(").nud = nud


def advance(id=None):
    global token
    if id and token.id != id:
        raise SyntaxError("Expected %r" % id)
    token = next(gen)


infix("+", 10)
infix("-", 10)
infix("*", 20)
infix("/", 20)
infix("^", 30)
prefix("+", 100)
prefix("-", 100)
prefix('func', 200)

symbol("(literal)").nud = lambda self: self
symbol("(end)")
symbol('(', 150)
symbol(')')
infix("<", 5); infix("<=", 5)
infix(">", 5); infix(">=", 5)
infix("<>", 5); infix("!=", 5); infix("=", 5)

token_pat = re.compile("(?:(\d+)|(\w+)|(\*\*|.))")


def tokenize(program):
    for number, func, operator in token_pat.findall(program):
        if number:
            # symbol = symbol_table['(literal)']
            # s = symbol()
            s = symbol_table['(literal)']()
            s.value = number
            yield s
        elif func:
            symbol = symbol_table['func']
            d = symbol()
            d.value = func
            yield d
        else:
            symbol = symbol_table.get(operator)
            if not symbol:
                raise SyntaxError('Unknown operator')
            yield symbol()
    symbol = symbol_table["(end)"]
    yield symbol()


def parse(program):
    global token, gen
    gen = tokenize(program)
    token = next(gen)
    return expression()


if __name__ == '__main__':
    print(parse('cos(2)'))