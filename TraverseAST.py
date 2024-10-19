from AstNodes import Program, Function, Return, Constant

class TraverseAST:
    def __init__(self):
        self.indentation = 0

    def print_with_indent(self, message):
        print(' ' * self.indentation + message)

    # Function to traverse and print the AST
    def traverse_ast(self, node):
        if isinstance(node, Program):
            for function in node.functions:
                self.traverse_ast(function)
        elif isinstance(node, Function):
            self.print_with_indent(f'Function: {node.name}')
            self.indentation += 2
            self.traverse_ast(node.body)
            self.indentation -= 2
        elif isinstance(node, Return):
            self.print_with_indent('Return Statement:')
            self.indentation += 2
            self.traverse_ast(node.exp)
            self.indentation -= 2
        elif isinstance(node, Constant):
            self.print_with_indent(f'Constant: {node.value}')
        else:
            self.print_with_indent('Unknown node type')
