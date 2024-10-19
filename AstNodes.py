class ASTNode:
    """Base class for all AST nodes."""
    pass

class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions  # List of Function nodes

class Function(ASTNode):
    def __init__(self, name, body):
        self.name = name  # Function name
        self.body = body  # Statement node

class Return(ASTNode):
    def __init__(self, exp):
        self.exp = exp  # Expression node

class Constant(ASTNode):
    def __init__(self, value):
        self.value = value  # The constant value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name  # The name of the identifier
