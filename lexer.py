import re
from enum import Enum, auto


class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    LOGICAL = auto()
    ASSIGN = auto()
    COMPARISON = auto()
    PUNCTUATION = auto()
    BOOLEAN = auto()
    EOF = auto()


KEYWORDS = {"if", "else", "while", "for", "do", "true", "false", "function"}

TOKEN_SPECIFICATION = [
    ("FLOAT", r'\d+\.\d+'),
    ("INTEGER", r'\d+'),
    ("STRING", r'\".*?\"'),
    ("BOOLEAN", r'\b(true|false)\b'),
    ("IDENTIFIER", r'[A-Za-z_]\w*'),
    ("LOGICAL", r'&&|\|\|'),
    ("COMPARISON", r'[<>]=?|==|!='),
    ("ASSIGN", r'='),
    ("OPERATOR", r'[+\-*/]'),
    ("PUNCTUATION", r'[;{}(),]'),
    ("SKIP", r'[ \t]+'),
    ("NEWLINE", r'\n'),
    ("COMMENT", r'#.*'),  # Добавлено правило для комментариев
    ("MISMATCH", r'.'),
]


class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.column = 0

    def tokenize(self):
        tokens = []
        for mo in re.finditer('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION), self.text):
            kind = mo.lastgroup
            value = mo.group(kind)
            start_column = self.column
            if kind == "NEWLINE":
                self.line += 1
                self.column = 0
                continue
            elif kind == "SKIP" or kind == "COMMENT":
                self.column += len(value)
                continue
            elif kind == "MISMATCH":
                raise SyntaxError(f"Недопустимый символ '{value}' в строке {self.line}, колонка {self.column}")
            elif kind == "IDENTIFIER" and value in KEYWORDS:
                kind = "KEYWORD"
            elif kind == "BOOLEAN":
                value = value == "true"

            token = (TokenType[kind], value, self.line, start_column)
            tokens.append(token)
            self.column += len(value)

        tokens.append((TokenType.EOF, None, self.line, self.column))
        return tokens
