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
from yaplVisImpl import DISPLACEMENTS

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


#TODO sacar los argumentos del stack al comenzar una función
#TODO list

class yaplVisCode(yaplVisitor):    

    def __init__(self):
        self.tag_count = 0
        self.const_count = 0
        self.temps = {}
        self.temp_count = 0
        self.current_func = None
        #for k, e in SYM_TABLE.items():
        #    print(f'{k}\t{e}')
        self.constructors = {}
        self.in_let = False

    def makeConst(self, val, var_type):
        const_name = f'const_{self.const_count}'
        self.const_count +=1
        for i in SYM_TABLE:
            if 'const_' in i:
                if SYM_TABLE[i]['const_val'] == val:
                    return SYM_TABLE[i]['ptr']
        SYM_TABLE[const_name] = {'type':var_type, 
                                'const_val':val, 'scope':{'global'}, 
                                'size':TYPE_TABLE[var_type]['size'],
                                'ptr':f"ptr_{self.current_scope}[{DISPLACEMENTS['global']}]"}
        DISPLACEMENTS['global'] += TYPE_TABLE[var_type]['size']
        return SYM_TABLE[const_name]['ptr']

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
        for i in self.constructors.values():
            code+= i
        if type(res) == list:
            for i in res:
                if type(i) == dict and 'code' in i:
                    code+= i['code'] + '\n'
        else:
            with open('out.ci', 'w') as f:
                f.write(res['code'])
            return res['code']
        with open('out.ci', 'w') as f:
            f.write(code)
        return code

    def visitIdentifier(self, ctx:yaplParser.IdentifierContext):
        name = f'{self.current_scope}.{ctx.getText()}'
        if name not in SYM_TABLE:
            name = f'{self.current_type}.{ctx.getText()}'
            if name not in SYM_TABLE:
                for i in reversed(range(1, FUNC_TABLE[self.current_func['name']]['lets']+1)):
                    name = f'{self.current_func["name"]}.{i}.{ctx.getText()}'
                    if name in SYM_TABLE:
                        break
        self.last_returned = SYM_TABLE[name]['type']
        code = f'\tlw {SYM_TABLE[name]["ptr"]}'

        assigned_on = []
        SYM_TABLE[name]['used'] = True
        if 'assigned_on' in SYM_TABLE[name]:
            assigned_on = SYM_TABLE[name]['assigned_on'].copy()
            if self.current_func and self.current_func['name'] in assigned_on:
                assigned_on.remove(self.current_func['name'])
        if 'const_val' in SYM_TABLE[name] \
            and (len(assigned_on) == 0 or 'known_val' in SYM_TABLE[name]):
            return {'code':code, 'res_temp':SYM_TABLE[name]['ptr'], 
                    'const_val':SYM_TABLE[name]['const_val'],
                    'comp':f"\tCMP {SYM_TABLE[name]['ptr']}, #1",
                    'branch_op':'BGE'}
        return {'code':code, 'res_temp':SYM_TABLE[name]['ptr'],
                    'comp':f"\tCMP {SYM_TABLE[name]['ptr']}, #1",
                    'branch_op':'BGE'}
    
    def visitVar_name(self, ctx:yaplParser.Var_nameContext):
        name = ctx.getText()
        name = f'{self.current_func["name"]}.{ctx.getText()}'
        if name not in SYM_TABLE:
            name = f'{self.current_type}.{ctx.getText()}'
        if name not in SYM_TABLE:
            name = f'{self.current_type}.{ctx.getText()}'
        if name not in SYM_TABLE:
            for i in reversed(range(1, FUNC_TABLE[self.current_func['name']]['lets']+1)):
                name = f'{self.current_func["name"]}.{i}.{ctx.getText()}'
                if name in SYM_TABLE:
                    break
        code = f'\tlw {SYM_TABLE[name]["ptr"]}'
        return {'code':code, 'res_temp':name}

    def visitBool_operation(self, ctx:yaplParser.Bool_operationContext):
        res = self.visitChildren(ctx)
        self.last_returned = self.current_type
        code = ''
        left = res[0]['res_temp']
        right = res[2]['res_temp']
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'
        code += f"\tCMP {left}, {right}"
        if res[1] == 'lt':
            branch_op = f'BLT'
        if res[1] == 'ltq':
            branch_op = f'BLE'
        if res[1] == 'eq':
            branch_op = f'BEQ'
        if 'const_val' in res[0] and 'const_val' in res[2]:
            if res[1] == 'lt':
                const_val = res[0]['const_val'] < res[2]['const_val']
            if res[1] == '<=':
                const_val = res[0]['const_val'] <= res[2]['const_val']
            if res[1] == '=':
                const_val = res[0]['const_val'] == res[2]['const_val']
            return {'comp':code, 'const_val':const_val, 'branch_op':branch_op}
        return {'comp':code, 'branch_op':branch_op}

    def visitWhile_loop(self, ctx:yaplParser.While_loopContext):
        res = self.visitChildren(ctx)
        condition = self.makeTag()
        loop = self.makeTag()
        code = f'\tb {condition}\n'
        code += f'{loop}:\n'
        res_t = ''
        for i in res:
            if type(i) == dict and 'res_temp' in i:
                res_t = i['res_temp']
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'
        code += f'{condition}:\n'
        for i in res:
            if type(i) == dict and 'branch_op' in i:
                branch_op = i['branch_op']
                break
        for i in res:
            if type(i) == dict and 'comp' in i:
                code+= i['comp'] + '\n'
                break
        code+= f'\t{branch_op} {loop}'

        return {'code':code, 'res_temp':res_t}
    
    def visitEos(self, ctx:yaplParser.EosContext):
        self.last_returned = self.current_type
        self.call_type = self.current_type
    
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
        self.current_scope = type_name
        self.temp_count = 0
        self.cons_temp = self.getTemp(8, type_name)
        type_size = TYPE_TABLE[type_name]['size']
        self.constructors[type_name] = f'{type_name}_constructor:\n'
        self.constructors[type_name] += '\tsw $ra, 0($sp) # store control flow registers in stack\n'
        self.constructors[type_name] += '\tsw $s0, 4($sp)\n'
        self.constructors[type_name] += '\tsw $s1, 8($sp)\n'
        self.constructors[type_name] += f'\n\tli $a0, {type_size}\n\tli $v0, 9\n\tmove {self.cons_temp}, $v0\n'

    def visitClass_grammar(self, ctx:yaplParser.Class_grammarContext):
        res = self.visitChildren(ctx)
        cons = self.constructors[self.current_type]
        cons += '\n\tlw $ra, 0($sp)        # read control flow  registers from stack\n'
        cons += '\tlw $s0, 4($sp)\n'
        cons += '\tlw $s1, 8($sp)\n'
        cons += f'\tsw {self.cons_temp}, 12($sp) # return initializated memory\n'
        cons += f'\tjr $ra\n'
        self.constructors[self.current_type] = cons
        return res

    def visitFunc_name(self, ctx:yaplParser.Func_nameContext):
        func_name = ctx.getText()
        call_namespace = self.class_name
        if self.call_type:
            call_namespace = self.call_type


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
        print(res)

        func_name = ''
        
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code += i['code'] + '\n'
                break
        
        for i in res:
            if type(i) == dict and 'func_name' in i:
                func_name = i['func_name']
                break
        args = ['parent_object']
        for i in res:
            if type(i) == dict and 'res_temp' in i:
                args.append(i['res_temp'])
                self.freeTemp(i['res_temp'])

        if type(res) == dict:
            args = res['params']
            func_name = res['func_name']
            if 'code' in res:
                code = res['code']
        
        ret_t = FUNC_TABLE[func_name]['ret_type']
        self.last_returned = ret_t
        # alocar 8 bytes por argumento, como se indica en:
        # https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/using-the-stack-in-aarch64-implementing-push-and-pop

        displacement = DISPLACEMENTS[func_name]
        code += f'\taddi sp, sp, -{4*displacement}\n'
        for i, arg in enumerate(args):
            code += f"\tsw {arg}, {4*(i+3)}($sp)\n"

        code+=f'\tjal {func_name}\n'
        ret_val = self.getTemp(TYPE_TABLE[ret_t]['size'], self.current_scope)

        code+= f'\tlw {ret_val}, {4*(displacement-1)}($sp)\n'
        
        code += f'\taddi sp, sp, {4*displacement}'
        return {'code':code, 'res_temp':ret_val}

    def visitLet_stmt(self, ctx:yaplParser.Let_stmtContext):
        self.in_let = True
        res = self.visitChildren(ctx)
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code += f'{i["code"]}\n'
        res_temp = ''
        for i in res:
            if type(i) == dict and 'res_temp' in i:
                res_temp = f'{i["res_temp"]}\n'
        self.in_let = False
        return {'code':code, 'res_temp':res_temp}

    def visitMem_name(self, ctx:yaplParser.Mem_nameContext):
        name = f'{self.current_type}.{ctx.getText()}'
        if self.in_let:
            for i in reversed(range(1, FUNC_TABLE[self.current_func['name']]['lets']+1)):
                name = f"{self.current_func['name']}.{i}.{ctx.getText()}"
                if name in SYM_TABLE:
                    break
        
        code = f'\tlw {SYM_TABLE[name]["ptr"]}\n'
        return {'varname': name, 'code':code}

    def visitMem_dec(self, ctx:yaplParser.Mem_decContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            code = res[0]['code']
            if len(res) > 2:
                if 'const_val' in res[2]:
                    SYM_TABLE[res[0]['varname']]['const_val'] = res[2]['const_val']
                    code += f"\tmov {SYM_TABLE[res[0]['varname']]['ptr']}, #{res[2]['const_val']}\n"
                else:
                    code += res[2]['code']
            code += f"\tstr {SYM_TABLE[res[0]['varname']]['ptr']}\n"
            self.constructors[self.current_type] += code

    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        val = ctx.getText()
        name = self.makeConst(val, STR)
        return {'res_temp':name, 'code':f'\tlw {name}\n'}

    def visitBool_literal(self, ctx:yaplParser.Bool_literalContext):
        val = ctx.getText()
        val = True if val == 'true' else False
        name = self.makeConst(val, BOOL)
        return {'res_temp':name, 'branch_op':'B', 'const_val':val, 'code':f'\tlw {name}\n'}

    def visitSign_dec(self, ctx:yaplParser.Sign_decContext):
        func_name = ctx.getText().split('(')[0]
        return {'code':f'{self.current_type}_{func_name}:'}

    def freeTemp(self, t):
        if t in self.temps:
            self.temps[t] = True

    def getTemp(self, size, scope):
        for k, e in self.temps.items():
            if e:
                self.temps[k] = False
                return k
        new_t = f'{scope}_t{self.temp_count}'
        SYM_TABLE[new_t] = {'size': size,
                            'scope':scope,
                            'ptr':f'ptr_{scope}[{DISPLACEMENTS[scope]}]'}
        DISPLACEMENTS[scope] += size
        self.temp_count+=1
        self.temps[new_t] = False
        return new_t
    
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        val = int(ctx.getText())
        name = self.makeConst(val, INT)
        #code = f'\tlw {name}'
        return {'res_temp':name, 'const_val':val, 'code':f'\tlw {name}\n'}

    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        res = self.visitChildren(ctx)
        code = ''
        self.freeTemp(res[0]['res_temp'])
        self.freeTemp(res[2]['res_temp'])

        op = res[1]
        temp = self.getTemp(4, self.current_func['name'])
        if 'const_val' in res[0] and 'const_val' in res[2]:
            if op == '+':
                const_val = res[0]['const_val'] + res[2]['const_val']
                code += f"\tLI {temp}, {const_val}"
            if op == '-':
                const_val = res[0]['const_val'] - res[2]['const_val']
                code += f"\tLI {temp}, {const_val}"
            if op == '*':
                const_val = res[0]['const_val'] * res[2]['const_val']
                code += f"\tLI {temp}, {const_val}"
            if op == '/':
                const_val = res[0]['const_val'] // res[2]['const_val']
                code += f"\tLI {temp}, {const_val}"

            return {'code':code, 'res_temp':temp, 'const_val':const_val}
        
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'
        
        if 'const_val' in res[0]:
            const_val = res[0]['const_val'] 
            if op == '+':
                code += f"\tADDI {temp}, {res[2]['res_temp']}, {const_val}"
            if op == '-':
                code += f"\tSUB {temp}, {res[2]['res_temp']}, #{const_val}"    #no existe en MIPS
            if op == '*':
                code += f"\tMUL {temp}, {res[2]['res_temp']}, #{const_val}"    #no existe en MIPS
            if op == '/':
                code += f"\tDIV {temp}, {res[2]['res_temp']}, #{const_val}"    #no existe en MIPS
            return {'code':code, 'res_temp':temp}
        
        if 'const_val' in res[2]:
            const_val = res[2]['const_val'] 
            if op == '+':
                code += f"\tADDI {temp}, {res[0]['res_temp']}, {const_val}"
            if op == '-':
                code += f"\tSUB {temp}, {res[0]['res_temp']}, #{const_val}"     #no existe en MIPS
            if op == '*': 
                code += f"\tMUL {temp}, {res[0]['res_temp']}, #{const_val}"     #no existe en MIPS
            if op == '/': 
                code += f"\tDIV {temp}, {res[0]['res_temp']}, #{const_val}"     #no existe en MIPS
            return {'code':code, 'res_temp':temp}



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
        self.freeTemp(res_temp)
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code+= i['code'] + '\n'

        if 'const_val' in res[1]:
            SYM_TABLE[assign_to]['const_val'] = res[1]['const_val']
            SYM_TABLE[assign_to]['known_val'] = True
            assign_to = SYM_TABLE[assign_to]['ptr']
            code+=f"\tMOV {assign_to}, #{res[1]['const_val']}\n"
            code+=f'\tSTR {assign_to}'

            return {'code':code, 'res_temp':res_temp}
        assign_to = SYM_TABLE[assign_to]['ptr']
        code+=f'\t{assign_to} = {res_temp}\n'
        code+=f'\tSTR {assign_to}'
        return {'code':code, 'res_temp':assign_to}

    def visitPlus_op(self, ctx:yaplParser.Plus_opContext):
        return PLUS

    def visitMinus_op(self, ctx:yaplParser.Minus_opContext):
        return MIN

    def visitDivision_op(self, ctx:yaplParser.Division_opContext):
        return DIV

    def visitMul_op(self, ctx:yaplParser.Mul_opContext):
        return MUL

    def visitFunc_body(self, ctx:yaplParser.Func_bodyContext):
        res = self.visitChildren(ctx)
        #for k, e in SYM_TABLE.items():
        #    if 'known_val' in e:
        #        del SYM_TABLE[k]['known_val']
        return res

    def visitFunc_dec(self, ctx:yaplParser.Func_decContext):
        func_name = ctx.getText().split('(')[0]
        self.current_func = {}
        self.current_func['name'] = self.current_type+'.'+func_name
        self.current_scope = self.current_func['name']
        self.temp_count = 0
        res = self.visitChildren(ctx)
        
        code = ''
        if type(res) == list:
            for i in res:
                code+=i['code'] + '\n'
        else:
            code = res['code']
        if self.current_func['name'] == 'Main.main':
            code+=f'\tli $v0, 10\n\tsyscall\n'
        return {'code':code}

    def visitIf_stmt(self, ctx:yaplParser.If_stmtContext):
        res = self.visitChildren(ctx)
        if 'const_val' in res[0]:
            if res[0]['const_val']:
                return res[1]
            return res[2]
        
        out_tag = self.makeTag()
        else_tag = self.makeTag()

        self.freeTemp(res[1]['res_temp'])
        self.freeTemp(res[2]['res_temp'])

        res_t = self.getTemp(8, self.current_scope)
        
        code = res[0]['comp'] + '\n'
        code+=f'\t{res[0]["branch_op"]} {else_tag}\n'
        if 'code' in res[2]:
            code+=res[2]['code'] + '\n'
        code+=f"\tMOV {res_t}, {res[2]['res_temp']}\n"
        code+=f'\tb {out_tag}\n'
        code+=f'{else_tag}:\n'
        if 'code' in res[1]:
            code+=res[1]['code'] + '\n'
        code+=f"\tMOV {res_t}, {res[1]['res_temp']}\n"
        code+=f'{out_tag}:'

        return {'code':code, 'res_temp':res_t}
    
    def visitRet_expr(self, ctx:yaplParser.Ret_exprContext):
        res = self.visitChildren(ctx)
        code = res['code'] + '\n'
        ret_val = res['res_temp']
        if self.current_func['name'] != 'Main.main':
            code+= f'\treturn {ret_val}'
        return {'code':code, 'res_temp':ret_val}
    
    def visitComp_expr(self, ctx:yaplParser.Comp_exprContext):
        res = self.visitChildren(ctx)
        code = ''
        ret_val = None
        #print(res)
        if type(res) == list:
            ret_val = res[-1]['res_temp']
            for i, e in enumerate(res):
                if 'code' in e:
                    if i < len(res)-1:
                        code += e['code'] + '\n'
                    else:
                        code += e['code'] 
        else:
            code = res['code']
            ret_val = res['res_temp']

        return {'code':code, 'res_temp':ret_val}

    def visitType(self, ctx:yaplParser.TypeContext):
        return {'type':ctx.getText()}

    def visitNew_call(self, ctx:yaplParser.New_callContext):
        res = self.visitChildren(ctx)
        
        func_name = f"{res['type']}_constructor"
        self.last_returned = res['type']
        
        code = ''

        args = []
        
        ret_t = res['type']
        # alocar 8 bytes por argumento, como se indica en:
        # https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/using-the-stack-in-aarch64-implementing-push-and-pop

        code += f'\tSUB sp, sp, #(8 * {func_name}_displacement)\n'
        for i, arg in enumerate(args):
            code += f"\tSTR {arg}, [sp, #(8 * {i+2})]\n"

        code+=f'\tcall {func_name}\n'
        
        ret_val = self.getTemp(TYPE_TABLE[ret_t]['size'], self.current_scope)

        code+= f'\tlw {ret_val}, [sp, #(8 * {func_name}_displacement-1)]\n'
        
        code += f'\tADD sp, sp, #(8 * {func_name}_displacement)'
        return {'code':code, 'res_temp':ret_val}

    def visitBigexpr(self, ctx:yaplParser.BigexprContext):
        res = self.visitChildren(ctx)

        func_name = ''
        
        code = ''
        for i in res:
            if type(i) == dict and 'code' in i:
                code += i['code'] + '\n'
                break
        
        for i in res:
            if type(i) == dict and 'func_name' in i:
                func_name = i['func_name']
                break
        args = []
        for i in res:
            if type(i) == dict and 'res_temp' in i:
                args.append(i['res_temp'])
                self.freeTemp(i['res_temp'])
        
        if type(res) == dict:
            args = res['params']
            func_name = res['func_name']
            if 'code' in res:
                code = res['code']
        
        ret_t = FUNC_TABLE[func_name]['ret_type']
        self.last_returned = ret_t
        # alocar 8 bytes por argumento, como se indica en:
        # https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/using-the-stack-in-aarch64-implementing-push-and-pop

        code += f'\tSUB sp, sp, #(8 * {func_name}_displacement)\n'
        for i, arg in enumerate(args):
            code += f"\tSTR {arg}, [sp, #(8 * {i+2})]\n"

        code+=f'\tcall {func_name}\n'
        ret_val = self.getTemp(TYPE_TABLE[ret_t]['size'], self.current_scope)

        code+= f'\tlw {ret_val}, [sp, #(8 * {func_name}_displacement-1)]\n'
        
        code += f'\tADD sp, sp, #(8 * {func_name}_displacement)'
        return {'code':code, 'res_temp':ret_val}

    def visitCalled_type(self, ctx:yaplParser.Called_typeContext):
        res = self.visitChildren(ctx)
        self.last_returned = res['type']

    def visitIsvoid(self, ctx:yaplParser.IsvoidContext):
        res = self.visitChildren(ctx)
        code = res['code']
        temp = self.getTemp(8, self.current_scope)
        code += f"\tSUB {temp}, {res['res_temp']}, #1\n"
        comp = f'\tCMP {temp}, #1\n'
        branch_op = 'BGE'
        return {'code':code, 'res_temp':temp, 
                'comp':comp, 'branch_op':branch_op}


    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        if 'comp' not in res:
            res['comp'] = f"\tCMP {res['res_temp']}, #1\n"
            res['branch_op'] = 'BGE'
        return res
del yaplVisitor