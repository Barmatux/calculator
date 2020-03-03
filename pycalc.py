from const_and_paterns import token_pattern, symbol_table
from symbol_classes import Lit, PostfixSymbol, Symbol


def tokenize(expression: str):
    """Tokenize our input string and make token one  of the given type"""
    for float_number, integer, function, operator in token_pattern.findall(expression):
        if float_number:
            yield Lit("lit", float(float_number), 0)
        if integer:
            yield Lit("lit", int(integer), 0)
        if function:
            yield PostfixSymbol("func", function, 200)
        if operator:
            op = symbol_table.get(operator)
            if not op:
                raise SyntaxError("Syntax's error this operation is not supported")
            yield op
    yield symbol_table['end']


def parse(inpt: str):
    Symbol.gen = tokenize(inpt)
    Symbol.token = next(Symbol.gen)
    return Symbol.expression()


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('EXPRESSION', nargs='+', help="expression string to evaluate")
    # name = 'EXPRESSION'
    # args = parser.parse_args()
    # inpt_lst_str = vars(args).get(name)
    # fr = ' '.join(inpt_lst_str)
    # print(parse('cos(-2+3*(-1))'))
    print(parse('+cos(90)'))


if __name__ == "__main__":
    main()
