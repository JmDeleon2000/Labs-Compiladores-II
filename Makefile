

PHONY: all

all: 
	antlr4-parse yapl.g4 yapl_src -tree test.yapl

gui: 
	antlr4-parse yapl.g4 yapl_src -gui test.yapl