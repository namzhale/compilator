from lexer import TokenType
from ast import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.current_token()[0] != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token_type, token_value = self.current_token()[0], self.current_token()[1]

        if token_type == TokenType.KEYWORD and token_value == "while":
            statement = self.parse_while()
        elif token_type == TokenType.KEYWORD and token_value == "if":
            statement = self.parse_if()
        elif token_type == TokenType.IDENTIFIER:
            statement = self.parse_assignment_or_variable()
        else:
            statement = self.expr()

        # Завершение обработки, если найден символ `;`
        if self.current_token()[0] == TokenType.PUNCTUATION and self.current_token()[1] == ";":
            self.consume()

        return statement

    def parse_if(self):
        """Разбирает условный оператор if с возможным else."""
        self.consume()  # Пропускаем 'if'
        self.consume(TokenType.PUNCTUATION, '(')  # Открывающая скобка для условия

        condition = self.expr()  # Условие if

        self.consume(TokenType.PUNCTUATION, ')')  # Закрывающая скобка для условия

        # Разбор основного блока if
        if_body = self.parse_block_or_statement()

        # Обработка возможного else
        else_body = None
        if self.current_token()[0] == TokenType.KEYWORD and self.current_token()[1] == "else":
            self.consume()  # Пропускаем 'else'
            else_body = self.parse_block_or_statement()

        return IfNode(condition, if_body, else_body)

    def parse_while(self):
        self.consume()  # Пропустить 'while'
        self.consume(TokenType.PUNCTUATION, '(')  # Открывающая скобка

        condition = self.expr()  # Условие цикла

        self.consume(TokenType.PUNCTUATION, ')')  # Закрывающая скобка

        body = self.parse_block_or_statement()
        return WhileNode(condition, body)

    def parse_block_or_statement(self):
        """Парсит либо блок кода в фигурных скобках, либо одиночное выражение."""
        if self.current_token()[0] == TokenType.PUNCTUATION and self.current_token()[1] == '{':
            return self.parse_block()
        else:
            return [self.parse_statement()]

    def parse_block(self):
        statements = []
        self.consume(TokenType.PUNCTUATION, '{')

        while not (self.current_token()[0] == TokenType.PUNCTUATION and self.current_token()[1] == '}'):
            statements.append(self.parse_statement())

        self.consume(TokenType.PUNCTUATION, '}')
        return statements

    def parse_assignment_or_variable(self):
        """Разбирает присваивание переменной или доступ к переменной."""
        var_name = self.current_token()[1]
        self.consume(TokenType.IDENTIFIER)

        if self.current_token()[0] == TokenType.ASSIGN:
            self.consume()
            value = self.expr()
            return VarAssignNode(var_name, value)
        else:
            return VarAccessNode(var_name)

    def expr(self):
        left = self.term()
        while self.current_token()[0] in {TokenType.COMPARISON, TokenType.LOGICAL} or \
                (self.current_token()[0] == TokenType.OPERATOR and self.current_token()[1] in ('+', '-')):
            op = self.consume()
            right = self.term()
            left = BinOpNode(left, op[1], right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token()[0] == TokenType.OPERATOR and self.current_token()[1] in ('*', '/'):
            op = self.consume()
            right = self.factor()
            left = BinOpNode(left, op[1], right)
        return left

    def factor(self):
        token = self.current_token()

        if token[0] == TokenType.INTEGER:
            self.consume()
            return NumberNode(int(token[1]))
        elif token[0] == TokenType.FLOAT:
            self.consume()
            return NumberNode(float(token[1]))
        elif token[0] == TokenType.IDENTIFIER:
            return self.parse_assignment_or_variable()
        elif token[0] == TokenType.PUNCTUATION and token[1] == '(':
            self.consume()
            expr = self.expr()
            self.consume(TokenType.PUNCTUATION, ')')
            return expr
        elif token[0] == TokenType.PUNCTUATION and token[1] == '{':
            return self.parse_block()  # парсинг вложенных блоков, если встретили `{`
        else:
            raise ValueError(f"Неожиданный токен {token[1]} ({token[0]}) в строке {token[2]}, колонка {token[3]}")

    def consume(self, expected_type=None, expected_value=None):
        token = self.current_token()

        if expected_type and token[0] != expected_type:
            raise ValueError(
                f"Ожидался токен типа {expected_type}, но найден {token[0]} на строке {token[2]}, колонка {token[3]}")
        if expected_value and token[1] != expected_value:
            raise ValueError(
                f"Ожидался токен '{expected_value}', но найден '{token[1]}' на строке {token[2]}, колонка {token[3]}")

        self.pos += 1
        return token

    def current_token(self):
        return self.tokens[self.pos]

    def peek_next_token(self):
        """Вспомогательный метод для просмотра следующего токена без потребления его."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return (TokenType.EOF, None)
