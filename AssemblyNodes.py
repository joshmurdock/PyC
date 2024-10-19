class AsmProgram:
    def __init__(self, function_definition):
        self.function_definition = function_definition

    def __str__(self):
        
        return f"{str(self.function_definition)}\n.section .note.GNU-stack,\"\",@progbits"

class AsmFunction:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions

    def __str__(self):
        result = [f"{self.name}:"]
        for instr in self.instructions:
            result.append(str(instr))
        return "\n".join(result)


class Mov:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return f"mov {self.src}, {self.dst}"


class Ret:
    def __str__(self):
        return "ret"


class Imm:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class Register:
    def __init__(self, name="%eax"):
        self.name = name

    def __str__(self):
        return self.name
