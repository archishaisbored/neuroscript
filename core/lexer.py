import re

KEYWORDS = {
    "remember", "update", "think", "while", "spiral", "feel", "otherwise",
    "speak", "shout", "whisper", "laugh", "panic", "pause", "murmur",
    "sleep", "listen"
}

def tokenize(code):
    print("Lexer: Starting tokenization")
    token_spec = [
        ('NUMBER',     r'\d+'),
        ('STRING',     r'"[^"\n]*"'),
        ('OP',         r'==|!=|<=|>=|[+\-*/<>]'),
        ('ASSIGN',     r'='),
        ('RANGE',      r'\.\.'),
        ('IDENT',      r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
        ('NEWLINE',    r'\n'),
        ('SKIP',       r'[ \t]+'),
        ('COMMENT',    r'#.*|//.*'),
        ('MISMATCH',   r'.'),
    ]

    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    get_token = re.compile(tok_regex).match

    pos = 0
    tokens = []
    indent_stack = [0]  # Stack to track indentation levels, starting at 0
    line_start = True
    expecting_block = False  # Flag to track if we're expecting an indented block (e.g., after 'feel' or 'otherwise')

    print(f"Lexer: Input code length = {len(code)}")
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise RuntimeError(f'Illegal character at {pos}')
        kind = match.lastgroup
        value = match.group()

        print(f"Lexer: Found token - {kind}: {value}")
        if kind == 'NEWLINE':
            tokens.append(('NEWLINE', '\n'))
            line_start = True
            expecting_block = False  # Reset after a newline unless a block starter was just seen
        elif kind == 'SKIP':
            if line_start:
                indent_level = len(value) // 4  # Assume 4 spaces per indent level
                current_indent = indent_stack[-1]

                if indent_level > current_indent:
                    indent_stack.append(indent_level)
                    tokens.append(('INDENT', indent_level))
                    print(f"Lexer: Added INDENT token, level {indent_level}")
                elif indent_level < current_indent:
                    while indent_level < indent_stack[-1]:
                        indent_stack.pop()
                        tokens.append(('DEDENT', indent_stack[-1]))
                        print(f"Lexer: Added DEDENT token, level {indent_stack[-1]}")
                    if indent_level != indent_stack[-1]:
                        raise RuntimeError(f'Inconsistent indentation at position {pos}')
            line_start = False
        elif kind == 'COMMENT':
            pass
        elif kind == 'STRING':
            tokens.append(('STRING', value.strip('"')))
            line_start = False
        elif kind == 'NUMBER':
            tokens.append(('NUMBER', int(value)))
            line_start = False
        elif kind == 'IDENT':
            if value in KEYWORDS:
                tokens.append(('KEYWORD', value))
                # If this keyword starts a block (e.g., 'feel', 'otherwise', 'think', 'while'), expect an indent
                if value in {'feel', 'otherwise', 'think', 'while'}:
                    expecting_block = True
            else:
                tokens.append(('IDENT', value))
            line_start = False
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Illegal character {value} at position {pos}')
        else:
            tokens.append((kind, value))
            line_start = False

        pos = match.end()

    # Ensure a NEWLINE before final DEDENTs and EOF
    if tokens and tokens[-1][0] != 'NEWLINE':
        tokens.append(('NEWLINE', '\n'))
        print("Lexer: Added final NEWLINE token")

    # Handle dedents at the end of the file
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', indent_stack[-1]))
        print(f"Lexer: Added final DEDENT token, level {indent_stack[-1]}")

    # Always append an EOF token
    tokens.append(('EOF', None))
    print("Lexer: Added EOF token")
    print(f"Lexer: Tokenization completed, tokens = {tokens}")
    return tokens