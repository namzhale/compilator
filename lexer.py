import re
from enum import Enum, auto


# Enum for token types, representing all possible categories of tokens
class TokenType(Enum):
    INTEGER = auto()  # Integer numbers
    FLOAT = auto()  # Floating-point numbers
    STRING = auto()  # Strings in double quotes
    IDENTIFIER = auto()  # Variable names or identifiers
    KEYWORD = auto()  # Reserved keywords (e.g., "if", "while")
    OPERATOR = auto()  # Arithmetic operators (+, -, *, /)
    LOGICAL = auto()  # Logical operators (&&, ||)
    ASSIGN = auto()  # Assignment operator (=)
    COMPARISON = auto()  # Comparison operators (<, >, <=, >=, ==, !=)
    PUNCTUATION = auto()  # Punctuation (e.g., ;, {}, (), commas)
    BOOLEAN = auto()  # Boolean values (true, false)
    EOF = auto()  # End of file/input marker


# Set of keywords for the language
KEYWORDS = {"if", "else", "while", "for", "do", "true", "false", "function"}

# Specification for matching each token type with a regular expression
TOKEN_SPECIFICATION = [
    ("FLOAT", r'\d+\.\d+'),  # Float numbers (e.g., 1.23)
    ("INTEGER", r'\d+'),  # Integer numbers (e.g., 123)
    ("STRING", r'\".*?\"'),  # Strings enclosed in double quotes
    ("BOOLEAN", r'\b(true|false)\b'),  # Boolean values (true or false)
    ("IDENTIFIER", r'[A-Za-z_]\w*'),  # Identifiers (variable/function names)
    ("LOGICAL", r'&&|\|\|'),  # Logical operators (&&, ||)
    ("COMPARISON", r'[<>]=?|==|!='),  # Comparison operators (<, >, <=, >=, ==, !=)
    ("ASSIGN", r'='),  # Assignment operator (=)
    ("OPERATOR", r'[+\-*/]'),  # Arithmetic operators (+, -, *, /)
    ("PUNCTUATION", r'[;{}(),]'),  # Punctuation symbols (e.g., ;, {}, (), ,)
    ("SKIP", r'[ \t]+'),  # Skip whitespace (spaces, tabs)
    ("NEWLINE", r'\n'),  # Newline to track line numbers
    ("COMMENT", r'#.*'),  # Comment (starts with # and goes to the end of the line)
    ("MISMATCH", r'.'),  # Any character that does not match any token (invalid token)
]


class Lexer:
    """
    Lexer for tokenizing input source code into a sequence of tokens.

    Attributes:
        text (str): The source code text to be tokenized.
        line (int): Current line number in the source code.
        column (int): Current column position within the line.
    """

    def __init__(self, text):
        """
        Initializes the lexer with the source code text.

        Args:
            text (str): The source code text to be tokenized.
        """
        self.text = text
        self.line = 1  # Start at the first line
        self.column = 0  # Start at the first column

    def tokenize(self):
        """
        Tokenizes the input text into a list of tokens, each with a type, value, line, and column.

        Returns:
            list of tuple: A list of tokens where each token is a tuple of:
                - TokenType: The type of the token (from the TokenType enum)
                - value: The value or literal content of the token
                - line: The line number where the token is found
                - start_column: The starting column position of the token

        Raises:
            SyntaxError: If an invalid character or sequence (mismatch) is encountered.
        """
        tokens = []  # List to store the identified tokens

        # Iterates through each match for the token patterns in TOKEN_SPECIFICATION
        for mo in re.finditer('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION), self.text):
            kind = mo.lastgroup  # Type of the matched token (e.g., INTEGER, IDENTIFIER)
            value = mo.group(kind)  # Actual value of the matched text
            start_column = self.column  # Starting column for this token

            if kind == "NEWLINE":
                # Handle newline by incrementing line number and resetting column
                self.line += 1
                self.column = 0
                continue
            elif kind == "SKIP" or kind == "COMMENT":
                # Ignore whitespace and comments (just update column position)
                self.column += len(value)
                continue
            elif kind == "MISMATCH":
                # Raise error for unmatched characters (invalid tokens)
                raise SyntaxError(f"Недопустимый символ '{value}' в строке {self.line}, колонка {self.column}")
            elif kind == "IDENTIFIER" and value in KEYWORDS:
                # Recognize keywords as separate from identifiers
                kind = "KEYWORD"
            elif kind == "BOOLEAN":
                # Convert boolean strings 'true'/'false' to Python booleans
                value = value == "true"

            # Create the token as a tuple with type, value, line, and start column
            token = (TokenType[kind], value, self.line, start_column)
            tokens.append(token)  # Add the token to the list
            self.column += len(value)  # Update column for next token

        # Append end-of-file token at the end of the input
        tokens.append((TokenType.EOF, None, self.line, self.column))
        return tokens
