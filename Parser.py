from AstNodes import Constant, Function, Program, Return


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.get_next_token()
        
    
    def get_next_token(self):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        else:
            return None  # No more tokens

    def eat(self, token_type, token_value=None):
        """Consume the current token if it matches the expected token type and value.
        
        Only uses type and value from tokens ignores rows and column"""
        if self.current_token:
            current_type = self.current_token[0]
            current_value = self.current_token[1]
            
            
            if current_type == token_type and (token_value is None or current_value == token_value):
                self.current_token = self.get_next_token()  # Move to the next token
                # Print the next token after moving forward
                if self.current_token:
                    print(f"After eating: Next token is ({self.current_token[0]}, {self.current_token[1]})")
                else:
                    print("After eating: No more tokens left.")
            else:
                raise SyntaxError(f"Expected token ({token_type}, {token_value}), got ({current_type}, {current_value})")
        else:
            raise SyntaxError("No more tokens")

    '''Context free grammar is defined and applied'''
    
    def parse(self):
        """Parse the entire program."""
        functions = []
        while self.current_token is not None:
            functions.append(self.parse_function())
        return Program(functions)
    
    def parse_function(self):
        """Parse a function definition."""
        self.eat('KEYWORD', 'int')  # Expect 'int' keyword for return type
        name = self.current_token[1]
        self.eat('IDENTIFIER')  # Expect function name (identifier)
        self.eat('PUNCTUATOR', '(')  # Expect '('

        # Handle the case where the parameter is 'void'
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'void':
            self.eat('KEYWORD', 'void')  # Consume the 'void' keyword

        self.eat('PUNCTUATOR', ')')  # Expect ')'
        self.eat('PUNCTUATOR', '{')  # Expect '{'
        body = self.parse_statement()  # Parse the function body (return statement)
        self.eat('PUNCTUATOR', '}')  # Expect '}'
        return Function(name, body)


    def parse_statement(self):
        """Parse a statement."""
        self.eat('KEYWORD', 'return')  # Expect 'return' keyword
        exp = self.parse_expression()
        self.eat('PUNCTUATOR', ';')  # Expect ';'
        return Return(exp)

    def parse_expression(self):
        """Parse an expression."""
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.eat('NUMBER')
            return Constant(value)
        else:
            raise SyntaxError(f"Expected NUMBER, got {self.current_token}")
