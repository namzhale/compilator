from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run(source_code, debug=False):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    if debug:
        print("Токены:")
        for token in tokens:
            print(token)
    parser = Parser(tokens)
    ast = parser.parse()
    if debug:
        print("\nAST:")
        for node in ast:
            print(node)
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    return result

if __name__ == "__main__":
    print("Введите код программы построчно. Для завершения ввода введите пустую строку.")
    lines = []
    while True:
        try:
            line = input()
            if line == '':
                break
            lines.append(line)
        except EOFError:
            break
    code = '\n'.join(lines)
    result = run(code)
    print("Результат выполнения программы:", result)
