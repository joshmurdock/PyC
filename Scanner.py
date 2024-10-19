import re

class Scanner:
    # Define C language keywords
    keywords = {
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
        'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return',
        'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
        'void', 'volatile', 'while'
    }

    # Define operators
    operators = {
        '+', '-', '*', '/', '%', '++', '--', '==', '!=', '<=', '>=', '<', '>', '=', '+=', '-=',
        '*=', '/=', '%=', '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '->', '.', '?', '::',
        '...', '&=', '|=', '^=', '<<=', '>>='
    }

    # Define regular expressions for tokens
    token_specification = [
        ('COMMENT',    r'//.*?$|/\*.*?\*/'),                     # Single-line and multi-line comments
        ('NEWLINE',    r'\n'),                                    # Line endings
        ('SKIP',       r'[ \t]+'),                                # Skip spaces and tabs
        ('NUMBER',     r'\d+(\.\d+)?'),                           # Integer or decimal number
        ('IDENTIFIER', r'[A-Za-z_]\w*'),                          # Identifiers
        ('STRING',     r'"([^"\\]|\\.)*"'),                       # String literals
        ('CHAR',       r"'(\\.|[^\\'])'"),                        # Character literals
        ('PUNCTUATOR', r'[()\[\]{};,]'),                          # Punctuation
        ('OPERATOR',   r'==|!=|<=|>=|<<=|>>=|<<|>>|\+\+|--|\+=|'
                       r'-=|\*=|/=|%=|&=|\|=|\^=|->|&&|\|\||::|\.|'
                       r'[-+*/%<>=!&|^~]'),                       # Operators
        ('MISMATCH',   r'.'),                                     # Any other character
    ]

    def __init__(self):
        self.token_regex = self.build_token_regex()
        self.token_regex_compiled = re.compile(self.token_regex, re.MULTILINE | re.DOTALL)

    # Builds a single regular expression from all the token patterns in token_specification
    def build_token_regex(self):
        token_patterns = []
        for spec in self.token_specification:
            name = spec[0]
            pattern = spec[1]
            token_patterns.append(f'(?P<{name}>{pattern})')
        return '|'.join(token_patterns)

    def tokenize(self, code):
        tokens = []
        line_number = 1
        line_start = 0
        # Use python's re to scan over the input code to find matches of the combined regex
        for match in self.token_regex_compiled.finditer(code):
            kind = match.lastgroup
            value = match.group(kind)
            column = match.start() - line_start
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
                tokens.append(('NUMBER', value, line_number, column))
            elif kind == 'IDENTIFIER':
                if value in self.keywords:
                    tokens.append(('KEYWORD', value, line_number, column))
                else:
                    tokens.append(('IDENTIFIER', value, line_number, column))
            elif kind in {'STRING', 'CHAR', 'PUNCTUATOR', 'OPERATOR'}:
                tokens.append((kind, value, line_number, column))
            elif kind == 'NEWLINE':
                line_start = match.end()
                line_number += 1
            elif kind in {'SKIP', 'COMMENT'}:
                continue
            elif kind == 'MISMATCH':
                # Raise an error for invalid tokens
                raise ValueError(f"Invalid character '{value}' at line {line_number}, column {column}")
        return tokens

    def scan(self, code):
        tokens = self.tokenize(code)
        return tokens

