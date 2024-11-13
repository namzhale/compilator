from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run(source_code, debug=False):
    """
    Runs the entire compilation and interpretation process on the provided source code.

    Args:
        source_code (str): The source code to be processed.
        debug (bool): If True, prints debugging information, including tokens and AST nodes.

    Returns:
        result: The final result of interpreting the source code.
    """

    # Step 1: Lexical Analysis (Tokenization)
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()  # Tokenize the input source code

    # Debug output for tokens
    if debug:
        print("Токены:")  # Output all tokens for debugging
        for token in tokens:
            print(token)

    # Step 2: Parsing (Building the AST)
    parser = Parser(tokens)
    ast = parser.parse()  # Parse tokens to generate the AST

    # Debug output for AST
    if debug:
        print("\nAST:")  # Output the AST for debugging
        for node in ast:
            print(node)

    # Step 3: Interpretation (Executing the AST)
    interpreter = Interpreter()
    result = interpreter.interpret(ast)  # Interpret the AST and get the result

    return result  # Return the result of the interpretation


# Example usage of the run function with a code sample and optional debug mode
if __name__ == "__main__":
    # Sample code to calculate 2^3 using a while loop
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
    # Run the code with debug mode disabled
    print("Результат выполнения программы:", run(code, debug=False))
