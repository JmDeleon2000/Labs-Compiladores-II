import sys
from antlr4 import *


from yaplLexer import yaplLexer
from yaplParser import yaplParser
from yaplVisImpl import yaplVisImpl
 
def main(argv):
    input_stream = FileStream(argv[1])
    print(f'Lexing:\n{input_stream}')
    lexer = yaplLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = yaplParser(stream)
    tree = parser.yapl_src()
    visitor = yaplVisImpl()
    res = visitor.visitYapl_src(tree.getRuleContext())
    print(res[1])
 
if __name__ == '__main__':
    main(sys.argv)