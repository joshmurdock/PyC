from AstNodes import Constant as AstConstant, Function as AstFunction, Program as AstProgram, Return as AstReturn
from AssemblyNodes import AsmFunction, AsmProgram, Mov, Ret, Imm, Register

'''Traverses the AST and generates corresponding assembly instructions'''

class AssemblyGenerator:
    def generate(self, node):
        """Generate assembly based on the AST node type."""
        if isinstance(node, AstProgram):
            # Handle multiple functions if needed
            return AsmProgram(self.generate(node.functions[0]))  # Assuming only a single function for now
        elif isinstance(node, AstFunction):
            instructions = []
            # Generate the body of the function
            instructions += self.generate(node.body)  # Make sure it's a flattened list
            return AsmFunction(node.name, instructions)
        elif isinstance(node, AstReturn):
            # Generate the instructions for return (Mov + Ret)
            return [Mov(self.generate(node.exp), Register()), Ret()]
        elif isinstance(node, AstConstant):
            # Return the immediate value (e.g., constant)
            return Imm(node.value)  # Constant becomes an immediate value
        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def get_assembly(self, assembly_ast):
        """Returns assembly instructions in a textual format."""

        return str(assembly_ast)  # Will call __str__ on the assembly_ast object
