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
        #for k, e in SYM_TABLE.items():
        #    print(f'{k}\t{e}')
        self.temps = {}
        self.temp_count = 0

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
        t = f'tag{self.tag_count}'
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
        code = f'\tld {name}'
        return {'code':code, 'res_temp':name}
    
    def visitVar_name(self, ctx:yaplParser.Var_nameContext):
        name = ctx.getText()
        code = f'\tld {name}'
        return {'code':code, 'res_temp':name}

    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        code = ''
        for i in res:
            if type(i) == dict:
                code+= i['code'] + '\n'
        code += f"\t{res[1]} {res[0]['res_temp']} {res[2]['res_temp']}"
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
        code+= f'\tjp {tag}'
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
    
    def visitEos(self, ctx:yaplParser.EosContext):
        self.last_returned = self.current_type
        self.call_type = self.current_type
        return self.visitChildren(ctx)
    
    def visitFree_func_name(self, ctx:yaplParser.Free_func_nameContext):
        self.call_type = self.current_type
        return self.visitChildren(ctx)
    
    def visitMark_last_t(self, ctx:yaplParser.Mark_last_tContext):
        res = self.visitChildren(ctx)
        self.call_type = self.last_returned
        return res
    
    def visitType_def(self, ctx:yaplParser.Type_defContext):
        type_name = ctx.getText()[5::]
        self.current_type = type_name
        self.class_name = type_name

    def visitFunc_name(self, ctx:yaplParser.Func_nameContext):
        func_name = ctx.getText()
        call_namespace = self.class_name
        if self.call_type:
            call_namespace = self.call_type

        if not call_namespace in TYPE_TABLE:
            err_msg = f"{bcolors.FAIL}Invalid function call to undeclared type: {call_namespace} {bcolors.ENDC}"
            print(err_msg)
            return (False, err_msg)
        #print(list(FUNC_TABLE.keys()))
        while call_namespace:
            #print(f'Searching for {func_name} in {call_namespace}')

            table_name = call_namespace+'.'+func_name
            if table_name in FUNC_TABLE and \
            table_name in TYPE_TABLE[call_namespace]['functions']:
                return {'ret_type':FUNC_TABLE[table_name]['ret_type'],
                               'params':FUNC_TABLE[table_name]['param_types'],
                               'func_name':table_name}
            call_namespace = TYPE_TABLE[call_namespace]['parent']

    def visitFunc_call(self, ctx:yaplParser.Func_callContext):
        res = self.visitChildren(ctx)
        
        func_name = ''
        
        for i in res:
            if type(i) == dict and 'func_name' in i:
                func_name = i['func_name']
        args = []
        for i in res:
            if type(i) == dict and 'res_temp' in i:
                args.append(i['res_temp'])
        ret_t = FUNC_TABLE[func_name]['ret_type']
        code = f'\ts_reserve {TYPE_TABLE[ret_t]["size"]}\n'
        for i in args:
            code+= f'\tstack {i}\n'
        code+=f'\tcall {func_name}'
        
        return {'code':code}


    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        return {'res_temp':self.makeConst(ctx.getText())}


    def visitSign_dec(self, ctx:yaplParser.Sign_decContext):
        func_name = ctx.getText().split('(')[0]
        return {'code':f'{self.current_type}_{func_name}:'}

    def freeTemp(self, t):
        self.temps[t] = True


    def getTemp(self):
        for k, e in self.temps.items():
            if e:
                self.temps[k] = False
                return k
        new_t = f't{self.temp_count}'
        self.temp_count+=1
        self.temps[new_t] = False
        return new_t
        

    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        res = self.visitChildren(ctx)
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'
        
        temp = self.getTemp()
        op = res[1]
        if op == '+':
            code += f"\tsum {temp} {res[0]['res_temp']} {res[2]['res_temp']}"
        if op == '-':
            code += f"\tmin {temp} {res[0]['res_temp']} {res[2]['res_temp']}"
        if op == '*':
            code += f"\tmul {temp} {res[0]['res_temp']} {res[2]['res_temp']}"
        if op == '/':
            code += f"\tdiv {temp} {res[0]['res_temp']} {res[2]['res_temp']}"
        
        return {'code':code, 'res_temp':temp}

    def visitAssignment(self, ctx:yaplParser.AssignmentContext):
        res = self.visitChildren(ctx)
        assign_to = res[0]['res_temp']
        res_temp = res[1]['res_temp']
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'

        code+=f'\t{assign_to} = {res_temp}'

        return {'code':code, 'res_temp':res_temp}

    def visitPlus_op(self, ctx:yaplParser.Plus_opContext):
        return PLUS

    def visitMinus_op(self, ctx:yaplParser.Minus_opContext):
        return MIN

    def visitDivision_op(self, ctx:yaplParser.Division_opContext):
        return DIV

    def visitMul_op(self, ctx:yaplParser.Mul_opContext):
        return MUL
del yaplVisitor