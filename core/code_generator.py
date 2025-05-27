class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, tac):
        self.instructions = []
        for instruction in tac:
            print(f"Processing TAC instruction: {instruction}")
            self.process_instruction(instruction)
        return self.instructions

    def process_instruction(self, instruction):
        parts = instruction.split(maxsplit=1)
        if not parts:
            return

        def emit_operand(operand):
            print(f"Evaluating operand: {operand}")
            if operand.isdigit():
                instr = f"PUSH {operand}"
            elif operand.startswith('"') and operand.endswith('"'):
                instr = f"PUSH {operand}"
            elif " " in operand and not operand.isdigit():
                instr = f'PUSH "{operand}"'
            else:
                instr = f"LOAD {operand}"
            print(f"Emitting operand instruction: {instr}")
            self.instructions.append(instr)

        if parts[0] in ("PRINT", "SHOUT", "WHISPER", "LAUGH", "MURMUR"):
            operand = parts[1] if len(parts) > 1 else ""
            emit_operand(operand)
            self.instructions.append(parts[0])
        elif parts[0] == "PANIC":
            message = instruction[len("PANIC "):].strip()
            self.instructions.append(f'PANIC {message}')
        elif parts[0] == "PAUSE":
            self.instructions.append("PAUSE")
        elif parts[0] == "SLEEP":
            self.instructions.append("SLEEP")
        elif parts[0] == "INPUT":
            prompt_end = instruction.rfind('"', 1)
            prompt = instruction[7:prompt_end]
            var = instruction[prompt_end+2:]
            self.instructions.append(f'INPUT "{prompt}" {var}')
        elif parts[0] == "LABEL":
            label = parts[1] if len(parts) > 1 else ""
            self.instructions.append(f"LABEL {label}")
        elif parts[0] == "JMP":
            label = parts[1] if len(parts) > 1 else ""
            self.instructions.append(f"JMP {label}")
        elif parts[0] == "JZ":
            subparts = parts[1].split(maxsplit=1)
            if len(subparts) == 2:
                emit_operand(subparts[0])
                self.instructions.append(f"JZ {subparts[1]}")
        else:
            # Handle assignments and binary operations
            assign_parts = instruction.split(" = ", 1)
            if len(assign_parts) == 2:
                target = assign_parts[0].strip()
                expr = assign_parts[1].strip()
                # Check if it's a binary operation
                # Handle quoted strings in binary operations properly
                if ' ADD ' in expr or ' SUB ' in expr or ' MUL ' in expr or ' DIV ' in expr or ' EQ ' in expr or ' NEQ ' in expr or ' LT ' in expr or ' GT ' in expr or ' LE ' in expr or ' GE ' in expr:
                    # Find the operation
                    operations = ["ADD", "SUB", "MUL", "DIV", "EQ", "NEQ", "LT", "GT", "LE", "GE"]
                    operation = None
                    for op in operations:
                        if f' {op} ' in expr:
                            operation = op
                            break

                    if operation:
                        # Split on the operation
                        parts = expr.split(f' {operation} ', 1)
                        if len(parts) == 2:
                            first_operand = parts[0].strip()
                            second_operand = parts[1].strip()
                            emit_operand(first_operand)
                            emit_operand(second_operand)
                            if operation == "ADD":
                                self.instructions.append("ADD")
                            elif operation == "SUB":
                                self.instructions.append("SUB")
                            elif operation == "MUL":
                                self.instructions.append("MUL")
                            elif operation == "DIV":
                                self.instructions.append("DIV")
                            elif operation == "EQ":
                                self.instructions.append("EQ")
                            elif operation == "NEQ":
                                self.instructions.append("NEQ")
                            elif operation == "LT":
                                self.instructions.append("LT")
                            elif operation == "GT":
                                self.instructions.append("GT")
                            elif operation == "LE":
                                self.instructions.append("LE")
                            elif operation == "GE":
                                self.instructions.append("GE")
                            self.instructions.append(f"STORE {target}")
                        else:
                            # Fallback to simple assignment
                            emit_operand(expr)
                            self.instructions.append(f"STORE {target}")
                    else:
                        # Simple assignment, e.g., x = 5
                        emit_operand(expr)
                        self.instructions.append(f"STORE {target}")
                else:
                    # Simple assignment, e.g., x = 5
                    emit_operand(expr)
                    self.instructions.append(f"STORE {target}")