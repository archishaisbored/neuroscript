from core.ast_nodes import (Program, VarDeclaration, Update, PrintCommand, Panic, Pause, Sleep,
                           InputCommand, IfStatement, WhileLoop, BinaryOperation, Literal, Variable)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', None)

    def advance(self):
        self.pos += 1

    def expect(self, token_type, token_value=None):
        token = self.current_token()
        if token[0] != token_type or (token_value is not None and token[1] != token_value):
            raise SyntaxError(f"Expected {token_type} {token_value or ''}, got {token}")
        self.advance()
        return token

    def parse(self):
        self.pos = 0
        program = Program([])
        while self.pos < len(self.tokens):
            token = self.current_token()
            if token[0] == 'EOF':
                break
            # Skip DEDENT tokens at the top level (can happen at the end of the file)
            if token[0] == 'DEDENT':
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
        return program

    def parse_statement(self):
        token = self.current_token()
        token_type, token_value = token

        print(f"Current token: {token} at position {self.pos}")  # Debug with position

        if token_type == 'KEYWORD':
            if token_value == 'remember':
                return self.parse_variable_declaration()
            elif token_value == 'update':
                return self.parse_update()
            elif token_value == 'think':
                return self.parse_while_loop()
            elif token_value == 'feel':
                return self.parse_if_statement()
            elif token_value == 'speak':
                self.advance()
                expr = self.parse_expression()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return PrintCommand('speak', expr)
            elif token_value == 'shout':
                self.advance()
                expr = self.parse_expression()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return PrintCommand('shout', expr)
            elif token_value == 'whisper':
                self.advance()
                expr = self.parse_expression()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return PrintCommand('whisper', expr)
            elif token_value == 'laugh':
                self.advance()
                expr = self.parse_expression()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return PrintCommand('laugh', expr)
            elif token_value == 'murmur':
                self.advance()
                expr = self.parse_expression()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return PrintCommand('murmur', expr)
            elif token_value == 'panic':
                self.advance()
                message = self.expect('STRING')[1]
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return Panic(message)
            elif token_value == 'pause':
                self.advance()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return Pause()
            elif token_value == 'sleep':
                self.advance()
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return Sleep()
            elif token_value == 'listen':
                self.advance()
                prompt = self.expect('STRING')[1]
                var = self.expect('IDENT')[1]
                if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                    self.advance()
                else:
                    self.expect('NEWLINE')
                return InputCommand(prompt, var)
            elif token_value == 'otherwise':
                raise SyntaxError(f"'otherwise' can only be used as part of an if statement")
        elif token_type == 'NEWLINE':
            self.advance()
            return None
        elif token_type == 'INDENT' or token_type == 'DEDENT':
            self.advance()
            return None

        raise SyntaxError(f"Unknown statement: {token_type} {token_value}")

    def parse_variable_declaration(self):
        self.advance()  # Consume 'remember'
        name = self.expect('IDENT')[1]
        self.expect('ASSIGN')
        # Check if the right-hand side is a 'listen' command
        if self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'listen':
            self.advance()  # Consume 'listen'
            prompt = self.expect('STRING')[1]
            if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
                self.advance()
            else:
                self.expect('NEWLINE')
            return VarDeclaration(name, InputCommand(prompt, name))
        # Otherwise, parse as a regular expression
        value = self.parse_expression()
        if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
            self.advance()
        else:
            self.expect('NEWLINE')
        return VarDeclaration(name, value)

    def parse_update(self):
        self.advance()  # Consume 'update'
        name = self.expect('IDENT')[1]
        self.expect('ASSIGN')
        value = self.parse_expression()
        if self.current_token()[0] in ('NEWLINE', 'DEDENT', 'EOF'):
            self.advance()
        else:
            self.expect('NEWLINE')
        return Update(name, value)

    def parse_while_loop(self):
        self.advance()  # Consume 'think'
        spiral = False
        if self.current_token()[1] == 'spiral':
            spiral = True
            self.advance()
        self.expect('KEYWORD', 'while')
        condition = self.parse_expression()
        self.expect('NEWLINE')
        body = self.parse_block()
        return WhileLoop(condition, body, spiral)

    def parse_if_statement(self):
        self.advance()  # Consume 'feel'
        print(f"Parsing if statement, condition start at position {self.pos}")
        condition = self.parse_expression()
        self.expect('NEWLINE')
        print(f"Parsing then block at position {self.pos}")
        then_block = self.parse_block()
        print(f"Finished then block at position {self.pos}, current token: {self.current_token()}")
        else_block = None

        # Skip any NEWLINE tokens before checking for 'otherwise'
        while self.current_token()[0] == 'NEWLINE':
            self.advance()
            print(f"Skipped NEWLINE before 'otherwise', now at position {self.pos}, token: {self.current_token()}")

        # Check for 'otherwise' and parse the else block
        if self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'otherwise':
            self.advance()  # Consume 'otherwise'
            print(f"Found 'otherwise' at position {self.pos}")
            self.expect('NEWLINE')
            print(f"Parsing else block at position {self.pos}")
            else_block = self.parse_block()
            print(f"Finished else block at position {self.pos}, current token: {self.current_token()}")

        # Consume any trailing NEWLINE after the if-else construct
        while self.current_token()[0] == 'NEWLINE':
            self.advance()
            print(f"Skipped trailing NEWLINE, now at position {self.pos}, token: {self.current_token()}")

        print(f"Finished if statement at position {self.pos}")
        return IfStatement(condition, then_block, else_block)

    def parse_block(self):
        statements = []
        print(f"Starting parse_block at position {self.pos}, token: {self.current_token()}")
        if self.current_token()[0] == 'INDENT':
            self.advance()  # Consume INDENT
            print(f"Consumed INDENT, now at position {self.pos}")
        else:
            print("No INDENT found, returning empty block")
            return statements

        while self.current_token()[0] not in ('DEDENT', 'EOF'):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        if self.current_token()[0] == 'DEDENT':
            self.advance()  # Consume DEDENT
            print(f"Consumed DEDENT, now at position {self.pos}")

        print(f"Finished parse_block at position {self.pos}, token: {self.current_token()}")
        return statements

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token()[0] == 'OP':
            op = self.current_token()[1]
            self.advance()
            right = self.parse_term()
            left = BinaryOperation(left, op, right)
        return left

    def parse_term(self):
        token = self.current_token()
        token_type, token_value = token

        if token_type == 'NUMBER':
            self.advance()
            return Literal(int(token_value))
        elif token_type == 'STRING':
            self.advance()
            return Literal(token_value)
        elif token_type == 'IDENT':
            self.advance()
            return Variable(token_value)
        else:
            raise SyntaxError(f"Invalid term: {token_type} {token_value}")