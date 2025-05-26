from core.ast_nodes import (Program, VarDeclaration, Update, PrintCommand, Panic, Pause, Sleep,
                           InputCommand, IfStatement, WhileLoop, BinaryOperation, Literal, Variable)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = set()

    def analyze(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.analyze(stmt)
        elif isinstance(node, VarDeclaration):
            # Analyze the value/expression on the right-hand side
            self.analyze(node.value)
            # Add variable to symbol table
            self.symbol_table.add(node.name)
        elif isinstance(node, Update):
            # Check if variable is declared
            if node.name not in self.symbol_table:
                raise SemanticError(f"Variable {node.name} not declared")
            # Analyze the value/expression
            self.analyze(node.value)
        elif isinstance(node, PrintCommand):
            # Analyze the expression to be printed
            self.analyze(node.expression)
        elif isinstance(node, Panic):
            # No variables to check in panic message (it's a string literal)
            pass
        elif isinstance(node, Pause):
            # No semantic checks needed
            pass
        elif isinstance(node, Sleep):
            # No semantic checks needed
            pass
        elif isinstance(node, InputCommand):
            # Add the variable to the symbol table (since listen assigns to it)
            self.symbol_table.add(node.var)
        elif isinstance(node, IfStatement):
            # Analyze the condition
            self.analyze(node.condition)
            # Analyze the then block
            for stmt in node.then_block:
                self.analyze(stmt)
            # Analyze the else block if it exists
            if node.else_block:
                for stmt in node.else_block:
                    self.analyze(stmt)
        elif isinstance(node, WhileLoop):
            # Analyze the condition
            self.analyze(node.condition)
            # Analyze the body (not block)
            for stmt in node.body:
                self.analyze(stmt)
        elif isinstance(node, BinaryOperation):
            self.analyze(node.left)
            self.analyze(node.right)
        elif isinstance(node, Literal):
            # No variables to check in literals
            pass
        elif isinstance(node, Variable):
            # Check if variable is declared
            if node.name not in self.symbol_table:
                raise SemanticError(f"Variable {node.name} not declared")

class SemanticError(Exception):
    pass