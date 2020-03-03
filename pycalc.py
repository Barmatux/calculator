from symbol_classes import base_symbol
from const_and_paterns import token_pattern, symbol_table, operator_table
from numbers import Number
import math
import argparse
from error_classes import Error


global token, gen




def expression(rbp=0):
    """ Main function that count result of expression"""
    global token, gen
    previous_token = token
    token = next(gen)
    left = previous_token.nud()
    while rbp < token.lbp:
        previous_token = token
        token = next(gen)
        if isinstance(left, Number) or left is None:
            left = previous_token.led(left)
        else:
            left = previous_token.led(left.value)
    if isinstance(left, Number):
        return left
    else:
        return left.value


def infix(oper_id, bp):
    """ reg operator, call class creation and make rule how to count it"""
    def count_left(oper, left):
        a = expression(bp)
        return operator_table[oper_id](left, a)
    make_symbol(oper_id, bp).led = count_left


def prefix(oper_id, bp):
    def count_value(exp):
        if exp.value == 'e' or exp.value == 'pi':
            return getattr(math, exp.value)
        if exp.oper_id == 'func':
            try:
                x = getattr(math, exp.value)
            except Exception:
                print(f'Unknown function {exp.value}')
                exit(-1)
            else:
                return x(expression(bp))
        a = expression(bp)
        if oper_id == '+':
            return a
        elif oper_id == '-':
            return -a
    make_symbol(oper_id).nud = count_value


def make_symbol(oper_id, bp=0):
    """Create new class  object from given oper_id and bp from symbol table,
    where we have registered all symbols or create new, and registrate it"""
    try:
        symbol = symbol_table[oper_id]
    except KeyError:
        class symbol(base_symbol):
            pass
        symbol.oper_id = oper_id
        symbol.lbp = bp
        symbol_table[oper_id] = symbol
    else:
        symbol.lbp = max(bp, symbol.lbp)
    return symbol


def nud_for_open_bracket(self):
    """ rule for bracket"""
    expr = expression()
    advance(")")
    return expr


make_symbol("(").nud = nud_for_open_bracket


def advance(oper_id=None):
    """ Check if we have close bracket, raise exception if no"""
    global token
    if oper_id and token.oper_id != oper_id:
        try:
            raise Error()
        except Error as e:
            print(e)
            exit(-1)
    token = next(gen)


def tokenize(inpt: str):
    """Tokenize our input string and make token one  of the given type"""
    for flt, integ,  func, operator in token_pattern.findall(inpt):
        if flt or integ:
            literal = symbol_table['lit']()
            if flt:
                literal.value = float(flt)
            else:
                literal.value = int(integ)
            yield literal
        elif func:
            s = symbol_table['func']()
            s.value = func
            yield s
        else:
            op = symbol_table.get(operator)
            if not op:
                try:
                    raise Error()
                except Error:
                    print('Syntaxis error')
                    exit(-1)
            yield op()
    symbol = symbol_table['end']()
    yield symbol


def parse(inpt: str):
    global gen, token
    gen = tokenize(inpt)
    token = next(gen)
    return expression()


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('EXPRESSION', nargs='+', help="expression string to evaluate")
    # name = 'EXPRESSION'
    # args = parser.parse_args()
    # inpt_lst_str = vars(args).get(name)
    # fr = ' '.join(inpt_lst_str)
    # print(parse('cos(-2+3*(-1))'))
    print(parse('-2-2'))


infix("+", 10)
infix("-", 10)
infix("*", 20)
infix("/", 20)
infix("//", 20)
infix("%", 20)
infix("^", 30)
prefix("+", 100)
prefix("-", 100)
prefix('func', 200)

make_symbol("lit").nud = lambda exp: exp
make_symbol("end")
make_symbol('(', 150)
make_symbol(')')
infix("<", 5); infix("<=", 5)
infix(">", 5); infix(">=", 5)
infix("!=", 5); infix("==", 5)

if __name__ == "__main__":
    main()
