import streamlit as st
from antlr4 import *


from yaplLexer import yaplLexer
from yaplParser import yaplParser
from yaplVisImpl import yaplVisImpl
from io import StringIO
import sys


def compile(text):
    with open('temp.txt', 'w') as f:
        f.write(text)
    input_stream = FileStream('temp.txt')

    lexer = yaplLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = yaplParser(stream)
    found_sintax_err = False
    f = StringIO()
    with f as sys.stderr:
        tree = parser.yapl_src()
        sintax_err = f.getvalue()
        if len(sintax_err) > 0:
            found_sintax_err = True
            st.markdown(f'''<span style='color:red'>{sintax_err}</span>''', unsafe_allow_html=True)
    
    if not found_sintax_err:
        visitor = yaplVisImpl()
        error_report = StringIO()
        with error_report as sys.stdout:
            res = visitor.visitYapl_src(tree.getRuleContext())
            
            if not res[0]:
                for l in error_report.getvalue().split('\n'):
                    out = l.replace('\033[91m', "<span style='color:red'>")
                    out = out.replace('\033[92m', "<span style='color:green'>")
                    out = out.replace('\033[0m', '</span>')
                    st.markdown(out, unsafe_allow_html=True)

        out = res[1].replace('\033[91m', "<span style='color:red'>")
        out = out.replace('\033[92m', "<span style='color:green'>")
        out = out.replace('\033[0m', '</span>')
        st.markdown(out, unsafe_allow_html=True)
    
    else:
        st.markdown("<span style='color:red'>Found sintax errors</span>", unsafe_allow_html=True)

st.title('Yes, this is Yet Another COOL compiler')

input_txt = st.text_area(label='Check it out:', value='''class Main inherits IO {
   main(): SELF_TYPE {
	out_string("Hello, World.\\n")
   };
};
''', height=420)

compile_input = st.button("Compile!")
if compile_input:
    try:
        compile(input_txt)
    except:
        st.markdown("<span style='color:red'>Sorry, that confused me!</br>There was an error, but I cannot tell what it is</span>", unsafe_allow_html=True)