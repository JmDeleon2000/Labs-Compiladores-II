# Generated from yapl.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .yaplParser import yaplParser
else:
    from yaplParser import yaplParser

from yaplVisitor import yaplVisitor

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ERR = 'error'
INT = 'int'
PLUS = '+'
MUL = '*'
DIV = '/'
MIN = '-'
ASIG = '<-'
BOOL = 'bool'
STR = 'string'
ANY = 'any'
SUPPORTED = {
    PLUS:[(INT, INT, INT),],
    DIV:[(INT, INT, INT),],
    MUL:[(INT, INT, INT),],
    MIN:[(INT, INT, INT),],
    ASIG:[(INT, INT, INT),
          (STR, STR, STR),
          (BOOL, BOOL, BOOL),
          (ANY, INT, INT),
          (ANY, STR, STR),
          (ANY, BOOL, BOOL),],
}

class yaplVisImpl(yaplVisitor):    
    
    # Visit a parse tree produced by yaplParser#yapl_src.
    def visitYapl_src(self, ctx:yaplParser.Yapl_srcContext):
        result = self.visitChildren(ctx)
        if type(result) == list:
            for i in result:
                if not i[0]:
                    return (False, f'{bcolors.FAIL}Build fail. Found errors.{bcolors.ENDC}')
        else:
            if not result[0]:
                return (False, f'{bcolors.FAIL}Build fail. Found errors.{bcolors.ENDC}')
        return (True, f'{bcolors.OKGREEN}Build success{bcolors.ENDC}')

    def visitAssignment(self, ctx:yaplParser.AssignmentContext):
        result = self.visitChildren(ctx)
        if type(result) == list:
            for i in result:
                if not i[0]:
                    return (False, i[1])
        else:
            if not result[0]:
                return (False, result[1])
        for i in SUPPORTED[result[1][1]]:
            if (i[0] == result[0][1] and 
                i[1] == result[2][1]):
                if i[0] != ANY:
                    return (True, i[0])
                return (True, i[2])
        err_str = (f'Cannot assign objects of type {result[2][1]} '
                f'to {result[0][1]} : {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        result = self.visitChildren(ctx)
        if type(result) == list:
            for i in result:
                if not i[0]:
                    return (False, i[1])
        else:
            if not result[0]:
                return (False, result[1])
        for i in SUPPORTED[result[1][1]]:
            if (i[0] == result[0][1] and 
                i[1] == result[2][1]):
                return (True, i[2])
        err_str = (f'Unsupported operation between {result[0][1]} '
                f'and {result[2][1]} for operator {result[1][1]}: {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)
    

    # Visit a parse tree produced by yaplParser#bool_literal.
    def visitBool_literal(self, ctx:yaplParser.Bool_literalContext):
        return (True, BOOL)


    # Visit a parse tree produced by yaplParser#str_literal.
    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        return (True, STR)

    # Visit a parse tree produced by yaplParser#int_literal.
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        return (True, INT)
    
    def visitPlus_op(self, ctx:yaplParser.Plus_opContext):
        return (True, PLUS)
    
        # Visit a parse tree produced by yaplParser#minus_op.
    def visitMinus_op(self, ctx:yaplParser.Minus_opContext):
        return (True, MIN)


    # Visit a parse tree produced by yaplParser#division_op.
    def visitDivision_op(self, ctx:yaplParser.Division_opContext):
        return (True, DIV)


    # Visit a parse tree produced by yaplParser#mul_op.
    def visitMul_op(self, ctx:yaplParser.Mul_opContext):
        return (True, MUL)
    
        # Visit a parse tree produced by yaplParser#assig_op.
    def visitAssig_op(self, ctx:yaplParser.Assig_opContext):
        return (True, ASIG)
    
    # Visit a parse tree produced by yaplParser#identifier.
    def visitIdentifier(self, ctx:yaplParser.IdentifierContext):
        return (True, ANY)

del yaplVisitor