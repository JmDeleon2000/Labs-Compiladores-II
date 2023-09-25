# Generated from yapl.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .yaplParser import yaplParser
else:
    from yaplParser import yaplParser

from yaplVisitor import yaplVisitor
from yaplVisImpl import SYM_TABLE
from yaplVisImpl import FUNC_TABLE
from yaplVisImpl import TYPE_TABLE

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    #OKGREEN = "<span style='color:green'>"
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    #FAIL = "<span style='color:red'>"
    #ENDC = '</span>'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

IO = 'IO'
OBJ = 'Object'
ERR = 'error'
INT = 'Int'
PLUS = '+'
MUL = '*'
DIV = '/'
MIN = '-'
LT = 'lt'
LTEQ = 'ltq'
EQUAL = 'eq'
ASIG = '<-'
BOOL = 'Bool'
STR = 'String'

CONSTS = []

class yaplVisCode(yaplVisitor):    

    def __init__(self):
        self.tag_count = 0
        self.const_count = 0

    def makeConst(self, val):
        const_name = f'c{self.const_count}'
        self.const_count +=1
        CONSTS.append((const_name, val))
        return const_name

    def visitEq(self, ctx:yaplParser.EqContext):
        return  EQUAL
    def visitLeq(self, ctx:yaplParser.LeqContext):
        return  LTEQ
    def visitLt(self, ctx:yaplParser.LtContext):
        return  LT

    def makeTag(self):
        t = f't{self.tag_count}'
        self.tag_count+=1
        return t

    def visitYapl_src(self, ctx:yaplParser.Yapl_srcContext):
        res = self.visitChildren(ctx)
        code = ''
        if type(res) == list:
            for i in res:
                if type(i) == dict and 'code' in i:
                    code+= i['code'] + '\n'
        else:
            return res['code']
        return code

    def visitIdentifier(self, ctx:yaplParser.IdentifierContext):
        name = ctx.getText()
        code = f'ld {name}'
        return {'code':code, 'res_temp':name}

    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        code = ''
        for i in res:
            if type(i) == dict:
                code+= i['code'] + '\n'
        code += f"{res[1]} {res[0]['res_temp']} {res[2]['res_temp']}"
        return {'comp':code}

    def visitWhile_loop(self, ctx:yaplParser.While_loopContext):
        res = self.visitChildren(ctx)
        tag = self.makeTag()
        code = f'{tag}:\n'
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'
        for i in res:
            if type(i) == dict and 'comp' in i:
                code+= i['comp'] + '\n'
        code+= f'jp {tag}'
        return {'code':code}

    def visitComp_expr(self, ctx:yaplParser.Comp_exprContext):
        res = self.visitChildren(ctx)
        code = ''
        if type(res) == list:
            for i in res:
                if type(i) == dict and 'code' in i:
                    code+= i['code'] + '\n'
        else:
            return res
        return {'code':code}
    

    def visitType_def(self, ctx:yaplParser.Type_defContext):
        type_name = ctx.getText()[5::]
        self.current_type = type_name



    def visitFunc_call(self, ctx:yaplParser.Func_callContext):
        res = self.visitChildren(ctx)
        print(self.current_type)
        func_name = ''
        print(FUNC_TABLE)
        for i in res:
            if type(i) == dict and 'func_name' in i:
                func_name = i['func_name']
        args = []
        for i in res:
            if type(i) == dict and 'res_temp' in i:
                args.append(i['res_temp'])
        ret_t = FUNC_TABLE[func_name]['ret_type']
        code = f's_reserve {ret_t}'
        
        return {'code':code}

    def visitFunc_name(self, ctx:yaplParser.Func_nameContext):
        func_name = ctx.getText()
        return {'func_name':func_name}

    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        return {'res_temp':self.makeConst(ctx.getText())}


del yaplVisitor