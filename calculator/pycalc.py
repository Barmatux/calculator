import argparse
from calculator.error_classes import CalcError
from calculator.const_and_paterns import token_pattern, symbol_table
from calculator.symbol_classes import Lit, PrefixSymbol, Symbol


def tokenize(expression: str):
    """Tokenize our input string and make token one  of the given type"""
    for float_number, integer, function, operator in token_pattern.findall(expression):
        if float_number:
            yield Lit("lit", float(float_number))
        if integer:
            yield Lit("lit", int(integer))
        if function:
            yield PrefixSymbol("func", function, 200)
        if operator:
            op = symbol_table.get(operator)
            if not op:
                raise CalcError("Error: this operation is not supported")
            yield op
    yield symbol_table['end']


def parse(inpt: str):
    Symbol.all_tokens = tokenize(inpt)
    Symbol.current_token = next(Symbol.all_tokens)
    return Symbol.current_token.count()


def read_consol():
    parser = argparse.ArgumentParser('Comand-line calculator')
    parser.add_argument('EXPRESSION', nargs='+', help="expression: string to evaluate")
    name = 'EXPRESSION'
    args = parser.parse_args()
    inpt_lst_str = vars(args).get(name)
    fr = ' '.join(inpt_lst_str)
    return (fr)


def print_output_to_console():
    print(parse('a'))


def main():
    try:
        print_output_to_console()
    except CalcError as e:
        print(e)


if __name__ == "__main__":
    main()
