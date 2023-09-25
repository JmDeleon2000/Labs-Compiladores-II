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
LT = '<'
LTEQ = '<='
EQUAL = '='
ASIG = '<-'
BOOL = 'Bool'
STR = 'String'
SUPPORTED = {
    PLUS:[(INT, INT, INT),],
    DIV:[(INT, INT, INT),],
    MUL:[(INT, INT, INT),],
    MIN:[(INT, INT, INT),],
    LT:[(INT, INT, BOOL),],
    LTEQ:[(INT, INT, BOOL),],
    EQUAL:[(INT, INT, BOOL),],
    ASIG:[(INT, INT, INT),
          (STR, STR, STR),
          (BOOL, BOOL, BOOL),],
}
CAN_BE_BOOL = [BOOL, INT, ]


out_string_info = {'param_types':[STR], 'ret_type':IO}
out_int_info = {'param_types':[INT], 'ret_type':IO}
type_name_info = {'param_types':[], 'ret_type':STR}
substr_info = {'param_types':[INT, INT], 'ret_type':STR}
abort_info = {'param_types':[], 'ret_type':OBJ}
TYPE_TABLE = {IO:   {'size':8, 'parent':OBJ, 'functions':[IO+'.'+'out_string',
                                                          IO+'.'+'out_int',
                                                          IO+'.'+'type_name']}, 
              BOOL: {'size':1, 'parent':OBJ, 'functions':[BOOL+'.'+'type_name']}, 
              STR:  {'size':8, 'parent':OBJ, 'functions':[STR+'.'+'substr', 
                                                          STR+'.'+'type_name']}, 
              INT:  {'size':4, 'parent':OBJ, 'functions':[INT+'.'+'type_name']}, 
              OBJ:  {'size':8, 'parent':None, 'functions':[OBJ+'.'+'type_name', 
                                                           OBJ+'.'+'abort']}}
SYM_TABLE = {}
FUNC_TABLE = {'IO.out_string':out_string_info,
                'IO.out_int':out_int_info,
                'String.substr':substr_info,
                'Object.type_name':type_name_info,
                'Object.abort':abort_info}
GLOBAL = 'global scope'

class yaplVisImpl(yaplVisitor):    

    def __init__(self):
        self.current_dis = 0
        self.current_class_dis = 0
        self.temp_to_name_map = dict()
        self.call_type = None
        self.calling_func = []
        self.current_func = None
        self.check_for_type_declaration = ['Main']
        self.check_for_func_declaration = ['Main.main']
        self.temp_count = 0
        self.temp_list = {}
    
    def getTemp(self):
        for k, free in self.temp_list.items():
            if free:
                self.temp_list[k] = False
                return k
        nt = f't{self.temp_count}'
        self.temp_count+=1
        self.temp_list[nt] = False
        return nt
    
    # Visit a parse tree produced by yaplParser#yapl_src.
    def visitYapl_src(self, ctx:yaplParser.Yapl_srcContext):
        print(f'{bcolors.WARNING}Reminder: All YAPL programs MUST include a declaration for the class Main. And that class MUST have a function called main{bcolors.ENDC}')
        print(f'{bcolors.OKGREEN}Compiling...{bcolors.ENDC}\n\n')
        res = self.visitChildren(ctx)
        if self.check_for_func_declaration:
            for i in self.check_for_func_declaration:
                if i == 'Main.main':
                    print(f'{bcolors.FAIL}All YAPL programs MUST include a declaration for the class Main. And that class MUST have a function called main{bcolors.ENDC}')
                else:
                    print(f'{bcolors.FAIL}You called {i}, but i cannot find the declaration for that function{bcolors.ENDC}')
            return (False, f'{bcolors.FAIL}Build failed. Found errors.{bcolors.ENDC}')
        if self.check_for_type_declaration:
            for i in self.check_for_type_declaration:
                if i == 'Main':
                    print(f'{bcolors.FAIL}All programs MUST include a class named {i}, but i cannot find the declaration for that class{bcolors.ENDC}')
                else:
                    print(f'{bcolors.FAIL}You created objects of class {i}, but i cannot find the declaration for that class{bcolors.ENDC}')
            return (False, f'{bcolors.FAIL}Build failed. Found errors.{bcolors.ENDC}')
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return (False, f'{bcolors.FAIL}Build failed. Found errors.{bcolors.ENDC}')
        else:
            if not res[0]:
                return (False, f'{bcolors.FAIL}Build failed. Found errors.{bcolors.ENDC}')
        return (True, f'{bcolors.OKGREEN}Build success{bcolors.ENDC}')

    def visitAssignment(self, ctx:yaplParser.AssignmentContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return (False, i[1])
        else:
            if not res[0]:
                return (False, res[1])
        
        var_name = res[0][1]
        if var_name not in SYM_TABLE:
            err_msg = f'{bcolors.FAIL}Cannot use variable "{var_name}" because it is not declared!{bcolors.ENDC}'
            print(err_msg)
            return (False, err_msg)
        var_t = SYM_TABLE[var_name]['type']
        expr_t = res[1][1]['type']
        
        for i in SUPPORTED[ASIG]:
            if (i[0] == var_t and 
                i[1] == expr_t):
                return (True, {'type':i[2]})
        err_str = (f'Cannot assign expresion of type {expr_t["type"]} '
                f'to {var_t}: {var_name}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#eos.
    def visitEos(self, ctx:yaplParser.EosContext):
        self.last_returned = self.current_type
        self.call_type = self.current_type
        return self.visitChildren(ctx)

    def visitEq(self, ctx:yaplParser.EqContext):
        return (True, EQUAL)
    def visitLeq(self, ctx:yaplParser.LeqContext):
        return (True, LTEQ)
    def visitLt(self, ctx:yaplParser.LtContext):
        return (True, LT)

    # Visit a parse tree produced by yaplParser#bool_operation.
    def visitBool_operation(self, ctx:yaplParser.Bool_operationContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return (False, i[1])
        else:
            if not res[0]:
                return (False, res[1])
        left_t = res[0][1]['type']
        right_t = res[2][1]['type']
        for i in SUPPORTED[res[1][1]]:
            if (i[0] == left_t and 
                i[1] == right_t):
                return (True, {'type': i[2]})
        err_str = (f'Unsupported operation between {left_t["type"]} '
                f'and {right_t["type"]} for operator {res[1][1]}: {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#arith_operation.
    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return (False, i[1])
        else:
            if not res[0]:
                return (False, res[1])
        left_t = res[0][1]['type']
        right_t = res[2][1]['type']
        for i in SUPPORTED[res[1][1]]:
            if (i[0] == left_t and 
                i[1] == right_t):
                return (True, {'type': i[2]})
        err_str = (f'Unsupported operation between {left_t} '
                f'and {right_t} for operator {res[1][1]}: {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#bool_literal.
    def visitBool_literal(self, ctx:yaplParser.Bool_literalContext):
        name = f'bool_lit_{ctx.getText()}'
        SYM_TABLE[name] = {'type':BOOL, 
                            'scope':{self.current_type, GLOBAL}, 
                            'size':1}
        temp = self.getTemp()
        return (True, {'type':BOOL, 'size':1,})

    # Visit a parse tree produced by yaplParser#paren.
    def visitParen(self, ctx:yaplParser.ParenContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return res
            self.last_returned = res[-1][1]['type']
            return (True, {'type':res[-1][1]['type']})
        if not res[0]:
            return res
        #self.last_returned = res[1]['type']
        return (True, {'type':res[1]['type']})

    # Visit a parse tree produced by yaplParser#str_literal.
    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        name = f'str_lit_{ctx.getText()}'
        SYM_TABLE[name] = {'type':STR, 
                            'scope':{self.current_type, GLOBAL}, 
                            'size':8}
        temp = self.getTemp()
        return (True,  {'type':STR, 'size':8,})

    # Visit a parse tree produced by yaplParser#int_literal.
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        name = f'int_lit_{ctx.getText()}'
        SYM_TABLE[name] = {'type':INT, 
                                        'scope':{self.current_type, GLOBAL}, 
                                        'size':4}
        return (True,  {'type':INT, 'size':4,})
    
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
    
    # Visit a parse tree produced by yaplParser#called_type.
    def visitCalled_type(self, ctx:yaplParser.Called_typeContext):
        res = self.visitChildren(ctx)
        self.last_returned = res[1]['type']
        return res

    # Visit a parse tree produced by yaplParser#mark_last_t.
    def visitMark_last_t(self, ctx:yaplParser.Mark_last_tContext):
        res = self.visitChildren(ctx)
        self.call_type = self.last_returned
        return res

    # Visit a parse tree produced by yaplParser#identifier.
    def visitIdentifier(self, ctx:yaplParser.IdentifierContext):
        txt = ctx.getText()
        new_id = txt
        if new_id in SYM_TABLE: # TODO check if accesible
            self.last_returned = SYM_TABLE[new_id]['type']
            return (True, {'type':SYM_TABLE[new_id]['type']})
        err_msg = f'{bcolors.FAIL}Cannot use variable "{txt}" because it is not declared!{bcolors.ENDC}'
        print(err_msg)
        return (False, err_msg)

    # Visit a parse tree produced by yaplParser#mem_name.
    def visitMem_name(self, ctx:yaplParser.Mem_nameContext):
        return (True, ctx.getText())

    def getDisplacement(self, size):
        current = self.current_dis
        self.current_dis+=size
        return current

    # Visit a parse tree produced by yaplParser#var_name.
    def visitVar_name(self, ctx:yaplParser.Var_nameContext):
        return (True, ctx.getText())

    # Visit a parse tree produced by yaplParser#mem_dec.
    def visitMem_dec(self, ctx:yaplParser.Mem_decContext):
        res = self.visitChildren(ctx)

        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])  

        var_name = res[0][1]

        if len(res) > 2:
            if res[1][1]['type'] != res[2][1]['type']:
                        err_msg = f'{bcolors.FAIL}Cannot assign expresion of type: {res[2][1]["type"]} to variable "{var_name}"! Expecting type: {res[1][1]["type"]}{bcolors.ENDC}'
                        print(err_msg)
                        return (False, err_msg)
            # type, scope, size, displacement, value
            SYM_TABLE[var_name] = {'type':res[1][1]['type'], 
                                                        'scope':{self.current_type, None}, 
                                                        'size':res[1][1]['size'], 
                                                        'displacement':self.getDisplacement(res[1][1]['size']),
                                                        'val_expr': None} #TODO

        # type, scope, size, displacement
        SYM_TABLE[var_name] = {'type':res[1][1]['type'], 
                                                        'scope':{self.current_type, None}, 
                                                        'size':res[1][1]['size'], 
                                                        'displacement':self.getDisplacement(res[1][1]['size']),
                                                        'val_expr': None}

        return (True, {'type':res[1]}) 
    


    # Visit a parse tree produced by yaplParser#scope_def.
    def visitComp_expr(self, ctx:yaplParser.Comp_exprContext):
        res = self.visitChildren(ctx)
        #self.cur_dis = 0
        #current_scope -= 1
        if type(res) == list:
            return res[-1]
        return res
    
    # Visit a parse tree produced by yaplParser#bool_expr.
    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        #Check if there was an error and spread it up the tree
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return res
        if not res[0]:
            return res
        self.last_returned = self.current_type
        if res[1]['type'] in CAN_BE_BOOL:
            return (True, {'type':BOOL})
        else:
            err_str = f'{bcolors.FAIL}Expected {ctx.getText()} to be a valid boolean expression {bcolors.ENDC}'
            print(err_str)
            return (False, err_str)
    
    # Visit a parse tree produced by yaplParser#inherited_type_def.
    def visitInherited_type_def(self, ctx:yaplParser.Inherited_type_defContext):
        res = self.visitChildren(ctx)
        TYPE_TABLE[res[0][1]]['parent'] = res[1][1]
        for i in TYPE_TABLE[res[1][1]]['functions']:
            TYPE_TABLE[res[0][1]]['functions'].append(i)
        return res[0]

    # Visit a parse tree produced by yaplParser#type.
    def visitType(self, ctx:yaplParser.TypeContext):
        name = ctx.getText()
        if name == 'SELF_TYPE':
            return (True, {'type':name, 'size':8})
        if name in TYPE_TABLE:
            return (True, {'type':name, 'size':TYPE_TABLE[name]['size']})
        self.current_type = name
        self.check_for_type_declaration.append(name)
        TYPE_TABLE[name] = {'size':8, 'parent':OBJ, 'functions':[]}
        return (True, {'type':name, 'size':8})

    def visitType_def(self, ctx:yaplParser.Type_defContext):
        type_name = ctx.getText()[5::]
        self.current_type = type_name
        TYPE_TABLE[type_name] = {'parent':OBJ}
        TYPE_TABLE[type_name]['functions'] = []
        TYPE_TABLE[type_name]['size'] = 8
        self.class_name = type_name
        self.call_type = self.class_name
        self.current_dis = 0
        SYM_TABLE['self'] = {'type':type_name, 
                            'scope':{self.current_type, None}, 
                            'size':8, 
                            'displacement':self.getDisplacement(8)}
        SUPPORTED[ASIG].append([type_name, type_name, type_name])
        if type_name in self.check_for_type_declaration:
            print(f'{bcolors.OKGREEN}Found the declaration for {type_name}!{bcolors.ENDC}')
            self.check_for_type_declaration.remove(type_name)
        return (True, type_name)
    
    def visitValid_inheritance(self, ctx:yaplParser.Valid_inheritanceContext):
        class_name = ctx.getText()
        if class_name in TYPE_TABLE:
            return (True, class_name)
        err_msg = f'{bcolors.FAIL}Cannot inheret from {class_name} because it was not previosly defined{bcolors.ENDC}'
        print(err_msg)
        return (False, err_msg)


    # Visit a parse tree produced by yaplParser#func_dec.
    def visitFunc_dec(self, ctx:yaplParser.Func_decContext):
        func_name = ctx.getText().split('(')[0]
        self.current_func = {}
        self.current_func['name'] = self.current_type+'.'+func_name
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by yaplParser#func_params.
    def visitFunc_params(self, ctx:yaplParser.Func_paramsContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) != list:
                res = [res]
            for i in res:
                SYM_TABLE[i['name']] = {'type':i['type'],
                                                    'scope':{self.current_type, self.current_func['name']},
                                                    'size':i['size'],
                                                    'displacement':self.getDisplacement(i['size']),}
        par_spec = []
        par_names = []
        if res:
            par_spec = [i['type'] for i in res]
            par_names = [i['name'] for i in res]
        return (True, {'param_types':par_spec, 'param_names':par_names})

    # Visit a parse tree produced by yaplParser#func_param.
    def visitFunc_param(self, ctx:yaplParser.Func_paramContext):
        res = self.visitChildren(ctx)
        return {'name':res[0][1], 'type':res[1][1]['type'], 'size':res[1][1]['size']}

    # Visit a parse tree produced by yaplParser#formal.
    def visitFormal(self, ctx:yaplParser.FormalContext):
        res = self.visitChildren(ctx)
        SYM_TABLE[res[0][1]] = {'type':res[1][1]['type'],
                                    'scope':{self.current_type, self.current_func['name']},
                                    'size':res[1][1]['size'],
                                    'displacement':self.getDisplacement(res[1][1]['size']),}
        return res 

    def GetCommonAncestor(self, type_a, type_b):

        temp_a = type_a
        while temp_a:
            temp_b = type_b
            while temp_b:
                if temp_a == temp_b:
                    return temp_a
                temp_b = TYPE_TABLE[temp_b]['parent']
            temp_a = TYPE_TABLE[temp_a]['parent']
        
        return None
    
    def CanImplicitCast(self, maybe_parent_type, type_b):
        temp_b = type_b
        while temp_b:
            if maybe_parent_type == temp_b:
                return maybe_parent_type
            temp_b = TYPE_TABLE[temp_b]['parent']

        if TYPE_TABLE[maybe_parent_type]['parent']:
            maybe_parent_type = TYPE_TABLE[maybe_parent_type]['parent']
            temp_b = type_b
            while temp_b:
                if maybe_parent_type == temp_b:
                    return maybe_parent_type
                temp_b = TYPE_TABLE[temp_b]['parent']
        
        return None

    # Visit a parse tree produced by yaplParser#ret_expr.
    def visitRet_expr(self, ctx:yaplParser.Ret_exprContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])   
        ret_type = self.current_func['ret_type']
        if ret_type == 'SELF_TYPE':
            ret_type = self.current_type
        expr_t = res[1]['type']


        ancestor = self.CanImplicitCast(ret_type, expr_t)
        if ancestor:
            return (True, ancestor)

        err_msg = (f"{bcolors.FAIL}Function {self.current_func['name']} cannot return " 
                f"'{ctx.getText()}' since it yields {expr_t}. Expecting {ret_type} or inheritor {bcolors.ENDC}")
        print(err_msg)
        return (False, err_msg)
    


    # Visit a parse tree produced by yaplParser#sign_dec.
    def visitSign_dec(self, ctx:yaplParser.Sign_decContext):
        res = self.visitChildren(ctx)
        func_name = ctx.getText().split('(')[0]
        table_name = self.current_type+'.'+func_name
        self.current_func['ret_type'] = res[1][1]['type']
        self.current_func['param_type'] = res[0][1]['param_types']
        func_info = {'param_types':res[0][1]['param_types'],
                    'ret_type':res[1][1]['type'],
                    'local':[table_name+'.ret_val'] + res[0][1]['param_names'],#TODO meter estos acá en let
                    'lets':0,#para diferenciar entre variables de diferentes lets
                    'new_calls':0}#para guardar espacio en el stack
        
        if table_name in self.check_for_func_declaration:
            print(f'{bcolors.OKGREEN}Found the declaration for {table_name}!{bcolors.ENDC}')
            self.check_for_func_declaration.remove(table_name)
        FUNC_TABLE[table_name] = func_info
        TYPE_TABLE[self.class_name]['functions'].append(table_name)
        return res
    

    # Visit a parse tree produced by yaplParser#while_loop.
    def visitWhile_loop(self, ctx:yaplParser.While_loopContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])     
        return (True, {'type':OBJ})

    # Visit a parse tree produced by yaplParser#if_stmt.
    def visitIf_stmt(self, ctx:yaplParser.If_stmtContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])     
        ancestor = self.GetCommonAncestor(res[1][1]['type'], res[2][1]['type'])
        return (True, {'type':ancestor})
    
    # Visit a parse tree produced by yaplParser#func_name.
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
                return (True, {'ret_type':FUNC_TABLE[table_name]['ret_type'],
                               'params':FUNC_TABLE[table_name]['param_types'],
                               'func_name':func_name})
            call_namespace = TYPE_TABLE[call_namespace]['parent']
        #reset call_namespace to original type
        call_namespace = self.class_name
        if self.call_type:
            call_namespace = self.call_type
        table_name = call_namespace+'.'+func_name
        warn_msg = f"{bcolors.WARNING}Called function {table_name} before it was declared! Proceeding expecting a declaration. {bcolors.ENDC}"
        print(warn_msg)
        TYPE_TABLE[f'{table_name}.ret_type'] = {'size':8, 'parent':OBJ}
        FUNC_TABLE[table_name] = {'param_types':'TBD', 'ret_type':f'{table_name}.ret_type'}
        self.check_for_func_declaration.append(table_name)
        return (True, {'ret_type':FUNC_TABLE[table_name]['ret_type'],
                        'params':FUNC_TABLE[table_name]['param_types'],
                        'func_name':table_name})

    # Visit a parse tree produced by yaplParser#func_call.
    def visitFunc_call(self, ctx:yaplParser.Func_callContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])     
        if type(res) == list:
            for i in res:
                if 'ret_type' in i[1]:
                    ret_type = i[1]['ret_type']
                    break
        else:
            ret_type = res[1]['ret_type']
        self.last_returned = ret_type
        return (True, {'type':ret_type})

    # Visit a parse tree produced by yaplParser#free_func_name.
    def visitFree_func_name(self, ctx:yaplParser.Free_func_nameContext):
        self.call_type = self.current_type
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by yaplParser#bigexpr.
    def visitBigexpr(self, ctx:yaplParser.BigexprContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1]) 

        expected_params = res[1][1]['params']
        ret_type = res[1][1]['ret_type']
        func_name = res[1][1]['func_name']
        recieved_params = [i[1]['type'] for i in res[2::] if 'type' in i[1]]
        if expected_params == 'TBD':
            expected_params = recieved_params
            FUNC_TABLE[func_name]['param_types'] = recieved_params
        if expected_params == None:
            expected_params = []
        if  expected_params == recieved_params:
            sz = TYPE_TABLE[ret_type]['size']
            self.last_returned = ret_type
            return (True, {'size':sz, 'type':ret_type})
        
        err_msg = f"{bcolors.FAIL}Function {func_name} doesn't take parameters: {recieved_params}. Expecting: {expected_params}{bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)

    # Visit a parse tree produced by yaplParser#new_call.
    def visitNew_call(self, ctx:yaplParser.New_callContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return res
        if not res[0]:
            return res
        self.last_returned = res[1]['type']
        FUNC_TABLE[self.current_func['name']]['new_calls'] +=1
        return (True, res[1])

    # Visit a parse tree produced by yaplParser#let_stmt.
    def visitLet_stmt(self, ctx:yaplParser.Let_stmtContext):
        FUNC_TABLE[self.current_type]['lets'] +=1
        res = self.visitChildren(ctx)
        if type(res) == list:
            res[-1]
        return res

    # Visit a parse tree produced by yaplParser#let_type_dec.
    def visitLet_type_dec(self, ctx:yaplParser.Let_type_decContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])  

        if type(res) != list:
            res = [res]

        let_count = FUNC_TABLE[self.current_func['name']]['lets']
        var_name = self.current_func['name']+f'.{let_count}.'+res[0][1]
        var_t = res[1][1]['type']
        var_sz = res[1][1]['size']
        # type, scope, size, displacement
        SYM_TABLE[var_name] = {'type':var_t, 
                                'scope':{self.current_func['name']}, 
                                'size':var_sz, 
                                'displacement':self.getDisplacement(var_sz)}
        if len(res) > 2:
            SYM_TABLE[var_name]['val_expr'] = None #TODO
        return SYM_TABLE[var_name]

    # Visit a parse tree produced by yaplParser#user_defined_t.
    def visitUser_defined_t(self, ctx:yaplParser.User_defined_tContext):
        print('in user defined t')
        type_name = ctx.getText()
        if type_name in TYPE_TABLE:
            return (True, type_name, TYPE_TABLE[type_name]['size'])
        warn_msg = f"{bcolors.WARNING}Used type {type_name} before it was declared. Proceeding expecting to find a declaration.{bcolors.ENDC}"
        print(warn_msg)
        TYPE_TABLE[type_name] = {'size':8, 'parent':OBJ, 'functions':[]}
        return (True, type_name, TYPE_TABLE[type_name]['size'])

    # Visit a parse tree produced by yaplParser#then.
    def visitThen(self, ctx:yaplParser.ThenContext):
        self.last_returned = self.current_type
        self.call_type = self.last_returned
        return self.visitChildren(ctx)

    # Visit a parse tree produced by yaplParser#else.
    def visitElse(self, ctx:yaplParser.ElseContext):
        self.last_returned = self.current_type
        self.call_type = self.last_returned
        return self.visitChildren(ctx)
