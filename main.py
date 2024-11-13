# main.py

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run(source_code, debug=False):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    if debug:
        print("Токены:")  # Отладочный вывод
        for token in tokens:
            print(token)

    parser = Parser(tokens)
    ast = parser.parse()

    if debug:
        print("\nAST:")  # Отладочный вывод
        for node in ast:
            print(node)

    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    return result


if __name__ == "__main__":
    code = """
    integ = 2;
    power = 3;
    result = 1;
    while (power > 0) {
        result = result * integ;
        power = power - 1;
    }
    result;
    """
    print("Результат выполнения программы:", run(code, debug=False))
