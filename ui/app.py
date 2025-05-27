import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from core.lexer import tokenize
from core.parser import Parser
from core.semantic_analyzer import SemanticAnalyzer
from core.tac_generator import TACGenerator
from core.code_generator import CodeGenerator
from core.vm import VirtualMachine
from core.utils import capture_output, pretty_print_tac, pretty_print_stack

def show_documentation():
    """Display NeuroScript documentation"""

    st.markdown("# NeuroScript - Code the way you think")

    st.markdown("## Introduction")
    st.markdown("""
    NeuroScript is a fun, expressive scripting language designed to simulate human mental flow - memory,
    reasoning, emotion, and reaction - through code.

    **Ideal for:**
    - Beginners learning logic
    - Fun compiler/interpreter projects
    - Demoing AST, interpreter pipelines
    - Experimental expressive programming
    """)

    st.markdown("## Basic Concepts")

    # Create a table for basic syntax
    syntax_data = [
        ["Declare variable", "remember", "remember x = 5"],
        ["Update variable", "update", "update x = x + 1"],
        ["Conditional", "feel", "feel x > 3"],
        ["Else", "otherwise", "-"],
        ["Loop", "think while", "think while x < 10"],
        ["Print", "speak", 'speak "Hello"'],
        ["End program", "sleep", "sleep"],
        ["Input", "listen", 'listen "What\'s your name?" name'],
        ["Comments", "# or //", "# this is a comment"]
    ]

    st.markdown("| **Concept** | **Keyword** | **Example** |")
    st.markdown("|-------------|-------------|-------------|")
    for row in syntax_data:
        st.markdown(f"| {row[0]} | `{row[1]}` | `{row[2]}` |")

    st.markdown("## Fun Keywords (Expressive Output)")

    fun_keywords = [
        ["shout", "Outputs message in uppercase"],
        ["whisper", "Outputs message in lowercase"],
        ["laugh", "Appends joy to the message"],
        ["panic", "Prints panic message and exits"],
        ["pause", "Adds a 1 sec delay"],
        ["spiral", "Use with `think spiral` for chaotic loops"],
        ["murmur", "Repeats message in a soft tone"]
    ]

    st.markdown("| **Keyword** | **Description** |")
    st.markdown("|-------------|-----------------|")
    for keyword, desc in fun_keywords:
        st.markdown(f"| `{keyword}` | {desc} |")

    st.markdown("## Control Flow Examples")

    st.markdown("### Conditional Example")
    st.code("""
remember age = 18
feel age >= 18
    speak "You can vote!"
otherwise
    speak "Too young to vote"
sleep
    """, language="text")

    st.markdown("### Loop Example")
    st.code("""
remember count = 5
think while count > 0
    speak "Countdown: " + count
    update count = count - 1
laugh "Blast off!"
sleep
    """, language="text")

    st.markdown("### Interactive Example")
    st.code("""
listen "What's your name? " name
listen "How old are you? " age
speak "Hello " + name + ", you are " + age + " years old!"
sleep
    """, language="text")

    st.markdown("## Sample Program")
    st.code("""
# NeuroScript voting eligibility checker
speak "Voting Eligibility Checker"
listen "Enter your age: " age

feel age >= 18
    shout "Congratulations! You are eligible to vote!"
    speak "Your civic duty awaits."
otherwise
    whisper "Sorry, you must be 18 or older to vote."
    speak "You have " + (18 - age) + " years to wait."

laugh "Thanks for using NeuroScript!"
sleep
    """, language="text")

    st.markdown("---")
    st.markdown("## The Developers")
    st.markdown("""
    **NeuroScript** was created by:
    - **Archisha Ghanshani**
    - **Priyanshi Mathur**
    - **Apoorva Dhiman**
    - **Abhay Das**
    """)

    st.markdown("---")
    st.markdown("*Ready to start coding? Click the back button or refresh to return to the compiler!*")

# Debug: Log when the app starts
print("App started at 01:47 AM IST on Tuesday, May 27, 2025")

st.set_page_config(page_title="NeuroScript Compiler", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: #e0e0e0;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.08, 0.92])
with col1:
    st.image("logo/neuron-logo.png", width=50)
with col2:
    st.markdown("# **NeuroScript**")
    st.caption("A thought-driven symbolic language")

st.markdown("---")

# Check if user wants to see documentation
query_params = st.query_params
show_docs = query_params.get("docs") == "true"

if show_docs:
    show_documentation()
    if st.button("← Back to Compiler"):
        st.query_params.clear()
        st.rerun()
    st.stop()

# Add a button to view documentation
if st.button("View Documentation"):
    st.query_params["docs"] = "true"
    st.rerun()

# Initialize session state
if "vm_output" not in st.session_state:
    st.session_state.vm_output = ""
    print("Session state initialized: vm_output set to empty string")





# Text area with no default code
code = st.text_area("Enter your NeuroScript code:", height=250, value="")

# Debug: Log when the button is clicked
if st.button("Run NeuroScript"):
    print("Run NeuroScript button clicked")
    st.session_state.vm_output = ""

    with st.expander("Lexical Analysis – Tokens"):
        try:
            print("Starting lexical analysis")
            tokens = tokenize(code)
            print(f"Lexical analysis completed: {len(tokens)} tokens generated")
            st.code(tokens, language='json')
        except Exception as e:
            print(f"Lexical analysis failed: {str(e)}")
            st.error(f"Lexical Error: {str(e)}")
            st.stop()

    with st.expander("Syntax Analysis – AST"):
        try:
            print("Starting syntax analysis")
            parser = Parser(tokens)
            print("Parser initialized")
            ast = parser.parse()
            print("Syntax analysis completed")
            st.code(str(ast), language='json')
        except Exception as e:
            print(f"Syntax analysis failed: {str(e)}")
            st.error(f"Syntax Error: {str(e)}")
            st.stop()

    with st.expander("Semantic Analysis"):
        try:
            print("Starting semantic analysis")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            print("Semantic analysis completed")
            st.success("Semantic checks passed")
        except Exception as e:
            print(f"Semantic analysis failed: {str(e)}")
            st.error(f"Semantic Error: {str(e)}")
            st.stop()

    with st.expander("TAC – Three Address Code"):
        try:
            print("Starting TAC generation")
            tac_gen = TACGenerator()
            tac = tac_gen.generate(ast)
            print(f"TAC generation completed: {len(tac)} instructions")
            st.code(pretty_print_tac(tac), language='text')
        except Exception as e:
            print(f"TAC generation failed: {str(e)}")
            st.error(f"TAC Error: {str(e)}")
            st.stop()

    with st.expander("Stack Code – Code Generator"):
        try:
            print("Starting code generation")
            cg = CodeGenerator()
            stack_code = cg.generate(tac)
            print(f"Code generation completed: {len(stack_code)} instructions")
            st.code(pretty_print_stack(stack_code), language='text')
        except Exception as e:
            print(f"Code generation failed: {str(e)}")
            st.error(f"Code Gen Error: {str(e)}")
            st.stop()

    with st.expander("Virtual Machine – Output"):
        try:
            print("Starting VM execution")
            vm = VirtualMachine()
            print("VM initialized")
            # Directly execute and capture output
            vm_output = vm.execute(stack_code, input_value=["Alice", "5"])
            print(f"VM execution completed: output = {vm_output}")
            st.session_state.vm_output = vm_output if vm_output else "(no output)"
            st.code(st.session_state.vm_output, language='text')
        except Exception as e:
            print(f"VM execution failed: {str(e)}")
            st.error(f"VM Error: {str(e)}")