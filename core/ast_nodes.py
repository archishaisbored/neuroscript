class Program:
    def __init__(self, statements):
        self.statements = statements

    def __str__(self):
        return "\n".join(str(stmt) for stmt in self.statements)

class VarDeclaration:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"VarDeclaration({self.name} = {self.value})"

class Update:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"Update({self.name} = {self.value})"

class PrintCommand:
    def __init__(self, command, expression):
        self.command = command  # 'speak', 'shout', 'whisper', 'laugh', 'murmur'
        self.expression = expression

    def __str__(self):
        return f"PrintCommand({self.command}, {self.expression})"

class Panic:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Panic({self.message})"

class Pause:
    def __init__(self):
        pass

    def __str__(self):
        return "Pause()"

class Sleep:
    def __init__(self):
        pass

    def __str__(self):
        return "Sleep()"

class InputCommand:
    def __init__(self, prompt, var):
        self.prompt = prompt
        self.var = var

    def __str__(self):
        return f"InputCommand({self.prompt}, {self.var})"

class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __str__(self):
        else_str = f"\nelse:\n  {self.else_block}" if self.else_block else ""
        return f"If({self.condition}):\n  {self.then_block}{else_str}"

class WhileLoop:
    def __init__(self, condition, body, spiral=False):
        self.condition = condition
        self.body = body
        self.spiral = spiral

    def __str__(self):
        prefix = "SpiralWhile" if self.spiral else "While"
        return f"{prefix}({self.condition}):\n  {self.body}"

class BinaryOperation:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class Literal:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Literal({self.value})"

class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Variable({self.name})"