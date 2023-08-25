

PHONY: tree

tree: 
	antlr4-parse yapl.g4 yapl_src -tree tests/test.yapl

gui: 
	antlr4-parse yapl.g4 yapl_src -gui tests/test.yapl

comp:
	antlr4 -Dlanguage=Python3 -visitor -no-listener yapl.g4

run_gui:
	streamlit run frontend.py