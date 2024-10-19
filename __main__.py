import os
import subprocess
import sys
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
        print(f"Compiling {preprocessed_file} to {assembly_file}")
        
        # Attempt to read the preprocessed file contents
        try:
            with open(preprocessed_file, "r") as f:
                file_contents = f.read()
        except FileNotFoundError:
            print(f"Error: Preprocessed file {preprocessed_file} not found.")
            return 1
        except IOError as e:
            print(f"Error reading preprocessed file {preprocessed_file}: {e}")
            return 1

        # Scan and parse the tokens
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
            return 1

        # Generate assembly code (should return an AsmProgram)
        try:
            generator = AssemblyGenerator()
            assembly_ast = generator.generate(ast)

            # Convert assembly AST to string
            assembly_code = generator.get_assembly(assembly_ast)

            # Ensure there's a newline at the end of the file
            if not assembly_code.endswith("\n"):
                assembly_code += "\n"
        except Exception as e:
            print(f"Error during assembly generation: {e}")
            return 1

        # Write the generated assembly code to the output file
        try:
            with open(assembly_file, "w") as f:
                f.write(assembly_code)
        except IOError as e:
            print(f"Error writing assembly file {assembly_file}: {e}")
            return 1


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
        
        # Read the content of the preprocessed file
        with open(preprocessed_file, 'r') as file:
            code = file.read()
        
        scanner = Scanner()
        tokens = scanner.scan(code)  
        # Print each token
        for token in tokens:
            print(token)


    def handle_parse(self, preprocessed_file):
        """Handle --parse option."""
        print("Running lexer and parser...")

        #Read the content of the preprocessed file
        with open(preprocessed_file, 'r') as file:
            code = file.read()
        
            # Tokenize the file content
            scanner = Scanner()
            tokens = scanner.scan(code)
            
            # Pass tokens to the parser
            parser = Parser(tokens)
            
            # Parse the tokens to produce an AST (Abstract Syntax Tree)
            ast = parser.parse()

            # Print AST
            ast_traversal = TraverseAST()
            ast_traversal.traverse_ast(ast)

    def handle_codegen(self, preprocessed_file):
        """Handle --codegen option."""
        print("Running code generation...")

    def handle_options(self, option, preprocessed_file):
        """Handle options using a mapping."""
        options = {
            "--lex": self.handle_lex,
            "--parse": self.handle_parse,
            "--codegen": self.handle_codegen
        }

        # If the option is valid, call the corresponding method
        if option in options:
            
            # Use first class object(dictionary) to call one of the options in handle_options
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
            # Step 1: Preprocess the source file (always needed)
            print("Preprocessing the input file...")
            return_code = self.preprocess(input_file, preprocessed_file)
            if return_code != 0:
                raise Exception("Preprocessing failed.")
        except Exception as e:
            print(f"Error during preprocessing: {e}")
            sys.exit(1)

        try:
            # Handle optional flags (--lex, --parse, --codegen)
            if option:
                print(f"Handling option: {option}")
                self.handle_options(option, preprocessed_file)
                self.clean_up([preprocessed_file])
                sys.exit(0)
        except Exception as e:
            print(f"Error while handling options: {e}")
            sys.exit(1)

        try:
            # Step 2: Compile the preprocessed file to assembly
            print("Compiling to assembly...")
            return_code = self.compile_to_assembly(preprocessed_file, assembly_file)
            if return_code != 0:
                raise Exception("Compilation to assembly failed.")
        except Exception as e:
            print(f"Error during assembly generation: {e}")
            self.clean_up([preprocessed_file])
            sys.exit(1)

        try:
            # Clean up the preprocessed file after compiling
            self.clean_up([preprocessed_file])
            
            # Handle the -S option (Stop after generating assembly)
            if option == "-S":
                print(f"Generated assembly file: {assembly_file}")
                sys.exit(0)
        except Exception as e:
            print(f"Error during cleanup after assembly generation: {e}")
            sys.exit(1)

        try:
            # Step 3: Assemble and link the assembly file to produce the executable
            print("Assembling and linking the assembly file...")
            return_code = self.assemble_and_link(assembly_file, output_file)
            if return_code != 0:
                raise Exception("Assembling and linking failed.")
        except Exception as e:
            print(f"Error during assembling and linking: {e}")
            self.clean_up([assembly_file])
            sys.exit(1)

        try:
            # Clean up the assembly file after linking
            self.clean_up([assembly_file])

            # Success
            print("Compilation succeeded.")
            sys.exit(0)
        except Exception as e:
            print(f"Error during cleanup after linking: {e}")
            sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: ./pyc_interface INPUT_FILE [OPTION]")
        sys.exit(1)

    input_file = sys.argv[1]
    option = sys.argv[2] if len(sys.argv) > 2 else None

    # Create an instance of the Interface class and run the process
    interface = Driver()
    interface.run(input_file, option)

if __name__ == "__main__":
    main()
