from core.ast_nodes import (Program, VarDeclaration, Update, PrintCommand, Panic, Pause, Sleep,
                           InputCommand, IfStatement, WhileLoop, BinaryOperation, Literal, Variable)

class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def generate(self, node):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0
        self.visit(node)
        return self.instructions

    def visit(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.visit(stmt)
        elif isinstance(node, VarDeclaration):
            result = self.visit(node.value)
            self.instructions.append(f"{node.name} = {result}")
            return node.name
        elif isinstance(node, Update):
            result = self.visit(node.value)
            self.instructions.append(f"{node.name} = {result}")
            return node.name
        elif isinstance(node, PrintCommand):
            result = self.visit(node.expression)
            if node.command == "speak":
                self.instructions.append(f"PRINT {result}")
            elif node.command == "shout":
                self.instructions.append(f"SHOUT {result}")
            elif node.command == "whisper":
                self.instructions.append(f"WHISPER {result}")
            elif node.command == "laugh":
                self.instructions.append(f"LAUGH {result}")
            elif node.command == "murmur":
                self.instructions.append(f"MURMUR {result}")
            return result
        elif isinstance(node, Panic):
            self.instructions.append(f'PANIC "{node.message}"')
        elif isinstance(node, Pause):
            self.instructions.append("PAUSE")
        elif isinstance(node, Sleep):
            self.instructions.append("SLEEP")
        elif isinstance(node, InputCommand):
            self.instructions.append(f'INPUT "{node.prompt}" {node.var}')
            return node.var
        elif isinstance(node, IfStatement):
            cond_result = self.visit(node.condition)
            else_label = self.new_label()
            end_label = self.new_label()

            # If condition is false, jump to else or end
            self.instructions.append(f"JZ {cond_result} {else_label}")

            # Then block - execute only if condition is true
            for stmt in node.then_block:
                self.visit(stmt)

            # Jump to end after then block (skip else block)
            self.instructions.append(f"JMP {end_label}")

            # Else block (or subsequent statements)
            self.instructions.append(f"LABEL {else_label}")
            if node.else_block:
                for stmt in node.else_block:
                    self.visit(stmt)

            # End of if statement
            self.instructions.append(f"LABEL {end_label}")
        elif isinstance(node, WhileLoop):
            start_label = self.new_label()
            end_label = self.new_label()

            # Start of loop
            self.instructions.append(f"LABEL {start_label}")

            # Evaluate condition
            cond_result = self.visit(node.condition)

            # If condition is false, jump to end
            self.instructions.append(f"JZ {cond_result} {end_label}")

            # Loop body
            for stmt in node.body:
                self.visit(stmt)

            # Jump back to start
            self.instructions.append(f"JMP {start_label}")

            # End of loop
            self.instructions.append(f"LABEL {end_label}")
        elif isinstance(node, BinaryOperation):
            left = self.visit(node.left)
            right = self.visit(node.right)
            temp = self.new_temp()

            if node.op == "+":
                self.instructions.append(f"{temp} = {left} ADD {right}")
            elif node.op == "-":
                self.instructions.append(f"{temp} = {left} SUB {right}")
            elif node.op == "*":
                self.instructions.append(f"{temp} = {left} MUL {right}")
            elif node.op == "/":
                self.instructions.append(f"{temp} = {left} DIV {right}")
            elif node.op == "==":
                self.instructions.append(f"{temp} = {left} EQ {right}")
            elif node.op == "!=":
                self.instructions.append(f"{temp} = {left} NEQ {right}")
            elif node.op == "<":
                self.instructions.append(f"{temp} = {left} LT {right}")
            elif node.op == ">":
                self.instructions.append(f"{temp} = {left} GT {right}")
            elif node.op == "<=":
                self.instructions.append(f"{temp} = {left} LE {right}")
            elif node.op == ">=":
                self.instructions.append(f"{temp} = {left} GE {right}")
            return temp
        elif isinstance(node, Literal):
            if isinstance(node.value, str):
                return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, Variable):
            return node.name