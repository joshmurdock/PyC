import os
import subprocess
import sys
import traceback
from Scanner import Scanner
from Parser import Parser
from AssemblyGenerator import AssemblyGenerator
from TraverseAST import TraverseAST


import os
import subprocess
import sys
import traceback
from Scanner import Scanner
from Parser import Parser
from AssemblyGenerator import AssemblyGenerator
from TraverseAST import TraverseAST

class Driver:
    def preprocess(self, input_file, preprocessed_file):
        """Run the preprocessor on the input file."""
        command = ["gcc", "-E", "-P", input_file, "-o", preprocessed_file]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Preprocessing failed: {result.stderr}")
            return result.returncode

        if not os.path.exists(preprocessed_file) or os.path.getsize(preprocessed_file) == 0:
            print("Preprocessing failed: Preprocessed file is missing or empty.")
            return 1

        return 0


    def compile_to_assembly(self, preprocessed_file, assembly_file):
        """Generate assembly file from the preprocessed file."""

        # Read and process the preprocessed file
        try:
            with open(preprocessed_file, "r") as f:
                file_contents = f.read()
        except (FileNotFoundError, IOError) as e:
            print(f"Error reading preprocessed file {preprocessed_file}: {e}")
            return 1

        # Scan and parse tokens
        try:
            scanner = Scanner()
            tokens = scanner.scan(file_contents)
            parser = Parser(tokens)
            ast = parser.parse()
        except SyntaxError as e:
            print(f"Syntax error during parsing: {e}")
            return 1
        except Exception as e:
            print(f"Error during scanning/parsing: {e}")
            traceback.print_exc()
            return 1

        # Generate assembly code
        try:
            generator = AssemblyGenerator()
            assembly_ast = generator.generate(ast)
            assembly_code = generator.get_assembly(assembly_ast)
            if not assembly_code.endswith("\n"):
                assembly_code += "\n"
        except Exception as e:
            print(f"Error during assembly generation: {e}")
            traceback.print_exc()
            return 1

        # Write to assembly file
        try:
            with open(assembly_file, "w") as f:
                f.write(assembly_code)
        except IOError as e:
            print(f"Error writing assembly file {assembly_file}: {e}")
            return 1

        return 0

    def assemble_and_link(self, assembly_file, output_file):
        """Run gcc to assemble and link the assembly file into an executable."""
        command = ["gcc", assembly_file, "-o", output_file]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Assembly and linking failed: {result.stderr}")
            return result.returncode
        return 0

    def handle_lex(self, preprocessed_file):
        """Handle --lex option."""
        print("Running lexer...")
        try:
            with open(preprocessed_file, 'r') as file:
                code = file.read()
            scanner = Scanner()
            tokens = scanner.scan(code)
            for token in tokens:
                print(token)
        except Exception as e:
            print(f"Error during lexing: {e}")

    def handle_parse(self, preprocessed_file):
        """Handle --parse option."""
        print("Running lexer and parser...")
        try:
            with open(preprocessed_file, 'r') as file:
                code = file.read()
            scanner = Scanner()
            tokens = scanner.scan(code)
            parser = Parser(tokens)
            ast = parser.parse()
            ast_traversal = TraverseAST()
            ast_traversal.traverse_ast(ast)
        except Exception as e:
            print(f"Error during parsing: {e}")

    def handle_codegen(self, preprocessed_file):
        """Handle --codegen option."""
        print("Running code generation...")

    def handle_options(self, option, preprocessed_file):
        """Map options to functions."""
        options = {
            "--lex": self.handle_lex,
            "--parse": self.handle_parse,
            "--codegen": self.handle_codegen
        }
        if option in options:
            options[option](preprocessed_file)
        else:
            print(f"Unknown option: {option}")

    def clean_up(self, files):
        """Remove intermediate files if they exist."""
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, input_file, option=None):
        """Run the compilation process."""
        base_name, _ = os.path.splitext(input_file)
        preprocessed_file = base_name + ".i"
        assembly_file = base_name + ".s"
        output_file = base_name

        try:
            print("Preprocessing the input file...")
            if self.preprocess(input_file, preprocessed_file) != 0:
                raise Exception("Preprocessing failed.")

            if option:
                print(f"Handling option: {option}")
                self.handle_options(option, preprocessed_file)
                self.clean_up([preprocessed_file])
                return

        
            if self.compile_to_assembly(preprocessed_file, assembly_file) != 0:
                raise Exception("Compilation to assembly failed.")

            self.clean_up([preprocessed_file])

            if option == "-S":
                print(f"Generated assembly file: {assembly_file}")
                return

            print("Assembling and linking the assembly file...")
            if self.assemble_and_link(assembly_file, output_file) != 0:
                raise Exception("Assembling and linking failed.")

            self.clean_up([assembly_file])
            print("Compilation succeeded.")
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.clean_up([preprocessed_file, assembly_file])
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./pyc_interface INPUT_FILE [OPTION]")
        sys.exit(1)

    input_file = sys.argv[1]
    option = sys.argv[2] if len(sys.argv) > 2 else None

    interface = Driver()
    interface.run(input_file, option)

if __name__ == "__main__":
    main()
