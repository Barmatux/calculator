import re

from symbol_classes import InfixSymbol, PostfixSymbol, Symbol, OpenBracket, Lit, PostfixInfixSymbol

symbol_table = {}

token_pattern = re.compile("(?:(\d*\.\d*)|(\d+)|(\w+)|(\<\=|\=\=|\>\=|\!\=|.))")


def make_symbol(id, bp=0, led=None, nud=None):
    """Create new class  object from given oper_id and bp from symbol table,
    where we have registered all symbols or create new, and registrate it"""
    symbol = symbol_table.get(id)
    if symbol:
        symbol.lbp = max(bp, symbol.lbp)
    else:
        if id == "+" or id == "-":
            symbol = PostfixInfixSymbol(id, 0, bp)
        elif led:
            symbol = InfixSymbol(id, 0, bp)
        elif nud:
            symbol = PostfixSymbol(id, 0, bp)
        elif id == "(":
            symbol = OpenBracket("(", 0, 150)
        elif id == "lit":
            symbol = Lit("lit", 0, 0)
        else:
            symbol = Symbol(id, 0, bp)
        symbol_table[id] = symbol
    return symbol


make_symbol("+", 10, led=True)
make_symbol("-", 10, led=True)
make_symbol("*", 20, led=True)
make_symbol("/", 20, led=True)
make_symbol("//", 2, led=True)
make_symbol("%", 20, led=True)
make_symbol("^", 30, led=True)
make_symbol("+", 100, nud=True)
make_symbol("-", 100, nud=True)
make_symbol('func', 200, nud=True)

make_symbol("lit")
make_symbol("end")
make_symbol('(', 150)
make_symbol(')')
make_symbol(',')
make_symbol("<", 5, led=True)
make_symbol("<=", 5, led=True)
make_symbol(">", 5, led=True)
make_symbol(">=", 5, led=True)
make_symbol("!=", 5, led=True)
make_symbol("==", 5, led=True)
