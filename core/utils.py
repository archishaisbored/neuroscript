def capture_output(func, *args, **kwargs):
    """
    Execute the function and return its return value.
    Debug prints will go to the terminal.
    """
    return func(*args, **kwargs)

def pretty_print_tac(tac):
    return "\n".join([f"{i}: {instr}" for i, instr in enumerate(tac)])

def pretty_print_stack(stack_code):
    return "\n".join([f"{i}: {instr}" for i, instr in enumerate(stack_code)])