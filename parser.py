from lexer import TokenType
from ast import *


class Parser:
    """
    Parser for transforming a list of tokens into an Abstract Syntax Tree (AST).

    Attributes:
        tokens (list): List of tokens to parse.
        pos (int): Current position in the tokens list.
    """

    def __init__(self, tokens):
        """
        Initializes the parser with the token list.

        Args:
            tokens (list): List of tokens produced by the lexer.
        """
        self.tokens = tokens
        self.pos = 0  # Position index in the token list

    def parse(self):
        """
        Parses all tokens into a list of statement nodes.

        Returns:
            list: A list of parsed AST nodes representing each statement in the source code.
        """
        statements = []
        # Continue parsing until the end-of-file token is encountered
        while self.current_token()[0] != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        """
        Parses a single statement, which could be a control structure, assignment, or expression.

        Returns:
            ASTNode: The parsed statement node.
        """
        token_type, token_value = self.current_token()[0], self.current_token()[1]

        # Check for control structures or assignments and call respective parse methods
        if token_type == TokenType.KEYWORD and token_value == "while":
            statement = self.parse_while()
        elif token_type == TokenType.KEYWORD and token_value == "if":
            statement = self.parse_if()
        elif token_type == TokenType.IDENTIFIER:
            statement = self.parse_assignment_or_variable()
        else:
            statement = self.expr()  # Default to parsing an expression

        # Consume the semicolon at the end of the statement if it exists
        if self.current_token()[0] == TokenType.PUNCTUATION and self.current_token()[1] == ";":
            self.consume()

        return statement

    def parse_if(self):
        """
        Parses an 'if' statement, including an optional 'else' clause.

        Returns:
            IfNode: An AST node representing the 'if' statement.
        """
        self.consume()  # Consume 'if' keyword
        self.consume(TokenType.PUNCTUATION, '(')  # Consume '(' symbol for condition

        condition = self.expr()  # Parse the 'if' condition as an expression

        self.consume(TokenType.PUNCTUATION, ')')  # Consume ')' symbol to end the condition

        # Parse the main 'if' block
        if_body = self.parse_block_or_statement()

        # Parse the optional 'else' block if present
        else_body = None
        if self.current_token()[0] == TokenType.KEYWORD and self.current_token()[1] == "else":
            self.consume()  # Consume 'else' keyword
            else_body = self.parse_block_or_statement()

        return IfNode(condition, if_body, else_body)

    def parse_while(self):
        """
        Parses a 'while' loop, including its condition and body.

        Returns:
            WhileNode: An AST node representing the 'while' loop.
        """
        self.consume()  # Consume 'while' keyword
        self.consume(TokenType.PUNCTUATION, '(')  # Consume '(' symbol for condition

        condition = self.expr()  # Parse the loop condition

        self.consume(TokenType.PUNCTUATION, ')')  # Consume ')' symbol to end the condition

        # Parse the body of the 'while' loop, which can be a block or single statement
        body = self.parse_block_or_statement()
        return WhileNode(condition, body)

    def parse_block_or_statement(self):
        """
        Parses either a block of statements enclosed in braces or a single statement.

        Returns:
            list: A list of AST nodes representing the block or single statement.
        """
        if self.current_token()[0] == TokenType.PUNCTUATION and self.current_token()[1] == '{':
            return self.parse_block()  # Parse a block of statements
        else:
            return [self.parse_statement()]  # Parse a single statement as a list

    def parse_block(self):
        """
        Parses a block of statements enclosed in curly braces.

        Returns:
            list: A list of AST nodes representing each statement in the block.
        """
        statements = []
        self.consume(TokenType.PUNCTUATION, '{')  # Consume '{' symbol to start the block

        # Parse each statement in the block until '}' is encountered
        while not (self.current_token()[0] == TokenType.PUNCTUATION and self.current_token()[1] == '}'):
            statements.append(self.parse_statement())

        self.consume(TokenType.PUNCTUATION, '}')  # Consume '}' symbol to end the block
        return statements

    def parse_assignment_or_variable(self):
        """
        Parses a variable assignment or variable access.

        Returns:
            VarAssignNode or VarAccessNode: A node representing either a variable assignment or access.
        """
        var_name = self.current_token()[1]
        self.consume(TokenType.IDENTIFIER)  # Consume the identifier (variable name)

        # Check if this is an assignment
        if self.current_token()[0] == TokenType.ASSIGN:
            self.consume()  # Consume '=' symbol
            value = self.expr()  # Parse the value to be assigned
            return VarAssignNode(var_name, value)  # Return an assignment node
        else:
            return VarAccessNode(var_name)  # Return a variable access node

    def expr(self):
        """
        Parses an expression, handling operators with lower precedence (e.g., +, -).

        Returns:
            ASTNode: A node representing the parsed expression.
        """
        left = self.term()
        # Parse operators like + and - or logical/comparison operators
        while self.current_token()[0] in {TokenType.COMPARISON, TokenType.LOGICAL} or \
                (self.current_token()[0] == TokenType.OPERATOR and self.current_token()[1] in ('+', '-')):
            op = self.consume()  # Consume the operator
            right = self.term()  # Parse the right operand
            left = BinOpNode(left, op[1], right)  # Combine into a binary operation node
        return left

    def term(self):
        """
        Parses a term, handling operators with higher precedence (e.g., *, /).

        Returns:
            ASTNode: A node representing the parsed term.
        """
        left = self.factor()
        # Parse * and / operators
        while self.current_token()[0] == TokenType.OPERATOR and self.current_token()[1] in ('*', '/'):
            op = self.consume()  # Consume the operator
            right = self.factor()  # Parse the right operand
            left = BinOpNode(left, op[1], right)  # Combine into a binary operation node
        return left

    def factor(self):
        """
        Parses a factor, which is the smallest unit in an expression (number, variable, or expression in parentheses).

        Returns:
            ASTNode: A node representing the parsed factor.

        Raises:
            ValueError: If an unexpected token is encountered.
        """
        token = self.current_token()

        # Handle numbers
        if token[0] == TokenType.INTEGER:
            self.consume()
            return NumberNode(int(token[1]))
        elif token[0] == TokenType.FLOAT:
            self.consume()
            return NumberNode(float(token[1]))

        # Handle variables
        elif token[0] == TokenType.IDENTIFIER:
            return self.parse_assignment_or_variable()

        # Handle expressions in parentheses
        elif token[0] == TokenType.PUNCTUATION and token[1] == '(':
            self.consume()
            expr = self.expr()
            self.consume(TokenType.PUNCTUATION, ')')  # Ensure closing parenthesis
            return expr

        # Handle blocks in braces (for nested block parsing)
        elif token[0] == TokenType.PUNCTUATION and token[1] == '{':
            return self.parse_block()

        # Error handling for unexpected tokens
        else:
            raise ValueError(f"Неожиданный токен {token[1]} ({token[0]}) в строке {token[2]}, колонка {token[3]}")

    def consume(self, expected_type=None, expected_value=None):
        """
        Consumes the current token if it matches the expected type and value.

        Args:
            expected_type (TokenType, optional): The expected type of the token.
            expected_value (str, optional): The expected value of the token.

        Returns:
            tuple: The consumed token.

        Raises:
            ValueError: If the current token does not match the expected type or value.
        """
        token = self.current_token()

        if expected_type and token[0] != expected_type:
            raise ValueError(
                f"Ожидался токен типа {expected_type}, но найден {token[0]} на строке {token[2]}, колонка {token[3]}")
        if expected_value and token[1] != expected_value:
            raise ValueError(
                f"Ожидался токен '{expected_value}', но найден '{token[1]}' на строке {token[2]}, колонка {token[3]}")

        self.pos += 1  # Move to the next token
        return token

    def current_token(self):
        """
        Retrieves the current token in the tokens list.

        Returns:
            tuple: The current token.
        """
        return self.tokens[self.pos]

    def peek_next_token(self):
        """
        Returns the next token without consuming it, useful for lookahead in parsing.

        Returns:
            tuple: The next token or (TokenType.EOF, None) if at the end.
        """
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return (TokenType.EOF, None)
