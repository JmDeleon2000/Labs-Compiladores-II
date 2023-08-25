import streamlit as st
from antlr4 import *


from yaplLexer import yaplLexer
from yaplParser import yaplParser
from yaplVisImpl import yaplVisImpl
import contextlib, io
import sys


def compile(text):
    with open('temp.txt', 'w') as f:
        f.write(text)
    input_stream = FileStream('temp.txt')
    lexer = yaplLexer(input_stream)
    stream = CommonTokenStream(lexer)
    with contextlib.redirect_stdout(f):
        parser = yaplParser(stream)

    tree = parser.yapl_src()
    visitor = yaplVisImpl()
    f = io.StringIO()
    #with contextlib.redirect_stdout(f):
    with open('report', 'w') as sys.stdout:
        res = visitor.visitYapl_src(tree.getRuleContext())
    
    st.markdown(res[1], unsafe_allow_html=True)
    if not res[0]:
        with open('report', 'r') as f:
            for l in f.readlines():
                st.markdown(l, unsafe_allow_html=True)

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
        st.write("Sorry, that confused me!\nThere was an error, but I cannot tell what it is")