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


class yaplVisCode(yaplVisitor):    

    def __init__(self):
        self.tag_count = 0
        self.const_count = 0
        self.temps = {}
        self.temp_count = 0
        self.current_func = None

    def makeConst(self, val, type):
        const_name = f'const_{self.const_count}'
        self.const_count +=1
        SYM_TABLE[const_name] = {'type':type, 'const_val':val, 'scope':{'global'}, 'size':TYPE_TABLE[type]['size']}
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
        #for k, e in SYM_TABLE.items():
        #    print(f'{k}\t{e}')
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
        assigned_on = []
        SYM_TABLE[name]['used'] = True
        if 'assigned_on' in SYM_TABLE[name]:
            assigned_on = SYM_TABLE[name]['assigned_on'].copy()
            if self.current_func['name'] in assigned_on:
                assigned_on.remove(self.current_func['name'])
        if 'const_val' in SYM_TABLE[name] and len(assigned_on) == 0:
            return {'code':code, 'res_temp':name, 'const_val':SYM_TABLE[name]['const_val']}
        return {'code':code, 'res_temp':name}
    
    def visitVar_name(self, ctx:yaplParser.Var_nameContext):
        name = ctx.getText()
        code = f'\tld {name}'
        return {'code':code, 'res_temp':name}

    def visitBool_operation(self, ctx:yaplParser.Bool_operationContext):
        res = self.visitChildren(ctx)
        code = ''
        left = res[0]['res_temp']
        right = res[2]['res_temp']
        for i in res:
            if type(i) == dict:
                code+= i['code'] + '\n'
        code += f"\tCMP {left}, {right}"
        if res[1] == 'lt':
            branch_op = f'BNE'
        if res[1] == '<=':
            branch_op = f'BNZ'
        if res[1] == '=':
            branch_op = f'BZ'
        if 'const_val' in res[0] and 'const_val' in res[2]:
            if res[1] == 'lt':
                const_val = res[0]['const_val'] < res[2]['const_val']
            if res[1] == '<=':
                const_val = res[0]['const_val'] <= res[2]['const_val']
            if res[1] == '=':
                const_val = res[0]['const_val'] == res[2]['const_val']
            return {'comp':code, 'const_val':const_val}
        return {'comp':code, 'branch_op':branch_op}

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
        code+= f'\tbne {tag}'
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

    def visitMem_name(self, ctx:yaplParser.Mem_nameContext):
        return ctx.getText()

    def visitMem_dec(self, ctx:yaplParser.Mem_decContext):
        res = self.visitChildren(ctx)
        if 'const_val' in res[1]:
            SYM_TABLE[res[0]]['const_val'] = res[1]['const_val']

    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        val = ctx.getText()
        name = self.makeConst(val, STR)
        return {'res_temp':name}


    def visitSign_dec(self, ctx:yaplParser.Sign_decContext):
        func_name = ctx.getText().split('(')[0]
        return {'code':f'{self.current_type}_{func_name}:'}

    def freeTemp(self, t):
        if t in self.temps:
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
    
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        val = int(ctx.getText())
        name = self.makeConst(val, INT)
        #code = f'\tld {name}'
        return {'res_temp':name, 'const_val':val}

    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        res = self.visitChildren(ctx)
        code = ''
        self.freeTemp(res[0]['res_temp'])
        self.freeTemp(res[2]['res_temp'])

        temp = self.getTemp()
        if 'const_val' in res[0] and 'const_val' in res[2]:
            op = res[1]
            if op == '+':
                const_val = res[0]['const_val'] + res[2]['const_val']
                code += f"\tMOV {temp}, #{const_val}"
            if op == '-':
                const_val = res[0]['const_val'] - res[2]['const_val']
                code += f"\tMOV {temp}, #{const_val}"
            if op == '*':
                const_val = res[0]['const_val'] * res[2]['const_val']
                code += f"\tMOV {temp}, #{const_val}"
            if op == '/':
                const_val = res[0]['const_val'] // res[2]['const_val']
                code += f"\tMOV {temp}, #{const_val}"
            add = f"\tMOV {temp} {const_val}"
            print(f'{ctx.getText()} to {add}')
            return {'code':code, 'res_temp':temp, 'const_val':const_val}
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'
        op = res[1]
        if op == '+':
            code += f"\tADD {temp}, {res[0]['res_temp']}, {res[2]['res_temp']}"
        if op == '-':
            code += f"\tSUB {temp}, {res[0]['res_temp']}, {res[2]['res_temp']}"
        if op == '*':
            code += f"\tMUL {temp}, {res[0]['res_temp']}, {res[2]['res_temp']}"
        if op == '/':
            code += f"\tdiv {temp}, {res[0]['res_temp']}, {res[2]['res_temp']}"

        
        return {'code':code, 'res_temp':temp}

    def visitAssignment(self, ctx:yaplParser.AssignmentContext):
        res = self.visitChildren(ctx)
        assign_to = res[0]['res_temp']
        res_temp = res[1]['res_temp']
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'

        if 'const_val' in res[1]:
            SYM_TABLE[assign_to]['const_val'] = res[1]['const_val']
            code+=f"\tMOV {assign_to}, #{res[1]['const_val']}\n"
            code+=f'\tstr {assign_to}'
            return {'code':code, 'res_temp':res_temp}

        code+=f'\t{assign_to} = {res_temp}\n'
        code+=f'\tstr {assign_to}'
        return {'code':code, 'res_temp':res_temp}

    def visitPlus_op(self, ctx:yaplParser.Plus_opContext):
        return PLUS

    def visitMinus_op(self, ctx:yaplParser.Minus_opContext):
        return MIN

    def visitDivision_op(self, ctx:yaplParser.Division_opContext):
        return DIV

    def visitMul_op(self, ctx:yaplParser.Mul_opContext):
        return MUL

    def visitFunc_dec(self, ctx:yaplParser.Func_decContext):
        func_name = ctx.getText().split('(')[0]
        self.current_func = {}
        self.current_func['name'] = self.current_type+'.'+func_name
        return self.visitChildren(ctx)

    def visitIf_stmt(self, ctx:yaplParser.If_stmtContext):
        res = self.visitChildren(ctx)
        if 'const_val' in res[0]:
            if res[0]['const_val']:
                return res[1]
            return res[2]
        
        out_tag = self.makeTag()
        else_tag = self.makeTag()
        
        code = res[0]['comp'] + '\n'
        code+=f'\t{res[0]["branch_op"]} {else_tag}\n'
        code+=res[1]['code'] + '\n'
        code+=f'\tb {out_tag}\n'
        code+=f'{else_tag}:\n'
        code+=res[2]['code'] + '\n'
        code+=f'{out_tag}:'

        return {'code':code}
del yaplVisitor