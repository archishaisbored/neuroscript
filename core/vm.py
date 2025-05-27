import time

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.labels = {}
        self.pc = 0
        self.output = []

    def _is_float(self, value):
        """Check if a string represents a valid float"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def execute(self, instructions, input_value=None):
        self.stack = []
        self.variables = {}
        self.labels = {}
        self.pc = 0
        self.output = []
        self.input_value = input_value if input_value else []
        self.input_index = 0

        for i, instr in enumerate(instructions):
            if instr.startswith("LABEL "):
                label = instr.split()[1]
                self.labels[label] = i

        while self.pc < len(instructions):
            instr = instructions[self.pc]
            print(f"Executing instruction at PC {self.pc}: {instr}")

            if instr.startswith('PUSH "'):
                opcode = "PUSH"
                end_quote = instr.rfind('"')
                if end_quote == -1 or end_quote <= 5:
                    raise ValueError(f"Malformed PUSH instruction: {instr}")
                args = instr[5:end_quote+1]
            elif instr.startswith('INPUT "'):
                opcode = "INPUT"
                end_quote = instr.rfind('"', 7, len(instr)-1)
                if end_quote == -1:
                    raise ValueError(f"Malformed INPUT instruction: {instr}")
                prompt = instr[7:end_quote]
                var = instr[end_quote+2:].strip()
                args = f'"{prompt}" {var}'
            elif instr.startswith('PANIC "'):
                opcode = "PANIC"
                args = instr[6:]
            elif instr.startswith('JZ '):
                opcode = "JZ"
                # JZ now has format "JZ label"
                parts = instr.split(maxsplit=1)
                args = parts[1] if len(parts) > 1 else ""
            else:
                parts = instr.split(maxsplit=1)
                opcode = parts[0]
                args = parts[1] if len(parts) > 1 else ""

            print(f"  Opcode: {opcode}, Args: {args}")

            if opcode == "PUSH":
                value = args
                if value.isdigit():
                    self.stack.append(int(value))
                    print(f"  Pushed numeric value: {value}")
                elif value.startswith('"') and value.endswith('"'):
                    self.stack.append(value[1:-1])
                    print(f"  Pushed string value: {value[1:-1]}")
                else:
                    raise ValueError(f"Invalid PUSH argument: {value}")
            elif opcode == "LOAD":
                var = args
                if var not in self.variables:
                    raise ValueError(f"Variable {var} not defined")
                self.stack.append(self.variables[var])
                print(f"  Loaded variable {var}: {self.variables[var]}")
            elif opcode == "STORE":
                var = args
                if not self.stack:
                    raise ValueError("Stack underflow on STORE")
                self.variables[var] = self.stack.pop()
                print(f"  Stored {self.variables[var]} in variable {var}")
            elif opcode == "ADD":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on ADD")
                b = self.stack.pop()
                a = self.stack.pop()
                if isinstance(a, str) or isinstance(b, str):
                    self.stack.append(str(a) + str(b))
                    print(f"  Concatenated {a} + {b} = {self.stack[-1]}")
                else:
                    self.stack.append(a + b)
                    print(f"  Added {a} + {b} = {self.stack[-1]}")
            elif opcode == "SUB":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on SUB")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                print(f"  Subtracted {a} - {b} = {self.stack[-1]}")
            elif opcode == "MUL":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on MUL")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                print(f"  Multiplied {a} * {b} = {self.stack[-1]}")
            elif opcode == "DIV":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on DIV")
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    raise ValueError("Division by zero")
                self.stack.append(a / b)
                print(f"  Divided {a} / {b} = {self.stack[-1]}")
            elif opcode == "EQ":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on EQ")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a == b else 0)
                print(f"  Compared {a} == {b}: {self.stack[-1]}")
            elif opcode == "NEQ":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on NEQ")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a != b else 0)
                print(f"  Compared {a} != {b}: {self.stack[-1]}")
            elif opcode == "LT":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on LT")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a < b else 0)
                print(f"  Compared {a} < {b}: {self.stack[-1]}")
            elif opcode == "GT":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on GT")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a > b else 0)
                print(f"  Compared {a} > {b}: {self.stack[-1]}")
            elif opcode == "LE":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on LE")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a <= b else 0)
                print(f"  Compared {a} <= {b}: {self.stack[-1]}")
            elif opcode == "GE":
                if len(self.stack) < 2:
                    raise ValueError("Stack underflow on GE")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a >= b else 0)
                print(f"  Compared {a} >= {b}: {self.stack[-1]}")
            elif opcode == "PRINT":
                if not self.stack:
                    raise ValueError("Stack underflow on PRINT")
                value = self.stack.pop()
                self.output.append(str(value))
                print(f"  Printed: {value}")
            elif opcode == "SHOUT":
                if not self.stack:
                    raise ValueError("Stack underflow on SHOUT")
                value = self.stack.pop()
                self.output.append(str(value).upper() + "!")
                print(f"  Shouted: {self.output[-1]}")
            elif opcode == "WHISPER":
                if not self.stack:
                    raise ValueError("Stack underflow on WHISPER")
                value = self.stack.pop()
                self.output.append(str(value).lower() + "...")
                print(f"  Whispered: {self.output[-1]}")
            elif opcode == "LAUGH":
                if not self.stack:
                    raise ValueError("Stack underflow on LAUGH")
                value = self.stack.pop()
                self.output.append(str(value) + "😂")
                print(f"  Laughed: {self.output[-1]}")
            elif opcode == "MURMUR":
                if not self.stack:
                    raise ValueError("Stack underflow on MURMUR")
                value = self.stack.pop()
                self.output.append(str(value).lower() + "... " + str(value).lower())
                print(f"  Murmured: {self.output[-1]}")
            elif opcode == "PANIC":
                message = args
                if message.startswith('"') and message.endswith('"'):
                    message = message[1:-1]
                raise ValueError(f"PANIC: {message}")
            elif opcode == "PAUSE":
                time.sleep(1)
                print("  Paused for 1 second")
            elif opcode == "SLEEP":
                print("  Sleeping (program end)")
                break
            elif opcode == "INPUT":
                prompt_end = args.rfind('"', 1)
                prompt = args[1:prompt_end]
                var = args[prompt_end+2:].strip()
                if self.input_index < len(self.input_value):
                    input_value = self.input_value[self.input_index]
                    # Try to convert to number if it looks like a number
                    if isinstance(input_value, str) and input_value.strip().isdigit():
                        self.variables[var] = int(input_value.strip())
                    elif isinstance(input_value, str) and self._is_float(input_value.strip()):
                        self.variables[var] = float(input_value.strip())
                    else:
                        self.variables[var] = input_value
                    self.input_index += 1
                    print(f"  Input {var} = {self.variables[var]}")
                else:
                    raise ValueError(f"No input provided for INPUT {var}")
            elif opcode == "JMP":
                label = args
                if label not in self.labels:
                    raise ValueError(f"Label {label} not found")
                self.pc = self.labels[label]
                print(f"  Jumped to label {label} at PC {self.pc}")
                continue
            elif opcode == "JZ":
                if not self.stack:
                    raise ValueError("Stack underflow on JZ")
                condition = self.stack.pop()
                # The label is now directly in args
                label = args
                if label not in self.labels:
                    raise ValueError(f"Label {label} not found")
                if condition == 0:
                    self.pc = self.labels[label]
                    print(f"  Jumped on zero to label {label} at PC {self.pc}")
                    continue
                print(f"  JZ condition {condition}, no jump")
            elif opcode == "LABEL":
                print(f"  Label {args}")
                pass
            else:
                raise ValueError(f"Unknown instruction: {instr}")

            self.pc += 1

        return "\n".join(self.output)