import sys
from antlr4 import *


from yaplLexer import yaplLexer
from yaplParser import yaplParser
from yaplVisImpl import yaplVisImpl
from yaplVisitorCode import yaplVisCode
 
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
    if res[0]:
        visitor_code = yaplVisCode()
        code = visitor_code.visitYapl_src(tree.getRuleContext())
        print(code)
 
if __name__ == '__main__':
    main(sys.argv)