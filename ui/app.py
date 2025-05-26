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
    st.caption("A thought-driven symbolic language 🧠")

st.markdown("---")

# Initialize session state
if "vm_output" not in st.session_state:
    st.session_state.vm_output = ""
    print("Session state initialized: vm_output set to empty string")

# Text area with no default code
code = st.text_area("📝 Enter your NeuroScript code:", height=250, value="")

# Debug: Log when the button is clicked
if st.button("Run NeuroScript 🚀"):
    print("Run NeuroScript button clicked")
    st.session_state.vm_output = ""

    with st.expander("🔍 Lexical Analysis – Tokens"):
        try:
            print("Starting lexical analysis")
            tokens = tokenize(code)
            print(f"Lexical analysis completed: {len(tokens)} tokens generated")
            st.code(tokens, language='json')
        except Exception as e:
            print(f"Lexical analysis failed: {str(e)}")
            st.error(f"Lexical Error: {str(e)}")
            st.stop()

    with st.expander("🧱 Syntax Analysis – AST"):
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

    with st.expander("🔎 Semantic Analysis"):
        try:
            print("Starting semantic analysis")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            print("Semantic analysis completed")
            st.success("Semantic checks passed ✓")
        except Exception as e:
            print(f"Semantic analysis failed: {str(e)}")
            st.error(f"Semantic Error: {str(e)}")
            st.stop()

    with st.expander("🛠️ TAC – Three Address Code"):
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

    with st.expander("⚙️ Stack Code – Code Generator"):
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

    with st.expander("🧠 Virtual Machine – Output"):
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