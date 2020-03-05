import re

from calculator.symbol_classes import InfixSymbol, PrefixSymbol, OpenBracket, Lit, PrefixInfixSymbol

token_pattern = re.compile("(?:(\d*\.\d*)|(\d+)|(\w+)|(\<\=|\=\=|\>\=|\!\=|.))")

symbol_table = {
    "+": PrefixInfixSymbol("+", 0, 10),
    "-": PrefixInfixSymbol("-", 0, 10),
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
    "func": PrefixSymbol('func', 0, 200)
}
