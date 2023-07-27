

PHONY: tree

tree: 
	antlr4-parse yapl.g4 yapl_src -tree test.yapl

gui: 
	antlr4-parse yapl.g4 yapl_src -gui test.yapl

comp:
	antlr4 -Dlanguage=Python3 -visitor -no-listener yapl.g4