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
    #OKGREEN = '\033[92m'
    OKGREEN = "<span style='color:green'>"
    WARNING = '\033[93m'
   # FAIL = '\033[91m'
    FAIL = "<span style='color:red'>"
    ENDC = '</span>'
    #ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

IO = 'IO'
OBJ = 'Object'
ERR = 'error'
INT = 'int'
PLUS = '+'
MUL = '*'
DIV = '/'
MIN = '-'
LT = '<'
LTEQ = '<='
EQUAL = '='
ASIG = '<-'
BOOL = 'bool'
STR = 'string'
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


out_string_info = {'args_types':[STR], 'ret_t':IO}
out_int_info = {'args_types':[INT], 'ret_t':IO}
type_name_info = {'args_types':[], 'ret_t':STR}
substr_info = {'args_types':[INT, INT], 'ret_t':STR}
TYPE_TABLE = {IO:   {'size':8, 'parent':OBJ, 'functions':{'out_string':out_string_info,
                                                          'out_int':out_int_info}}, 
              BOOL: {'size':1, 'parent':OBJ, 'functions':dict()}, 
              STR:  {'size':8, 'parent':OBJ, 'functions':{'substr':substr_info}}, 
              INT:  {'size':4, 'parent':OBJ, 'functions':dict()}, 
              OBJ:  {'size':8, 'parent':None, 'functions':{'type_name':type_name_info}}}


class yaplVisImpl(yaplVisitor):    

    def __init__(self):
        self.current_scope = {'id': 0, 'name': 'global', 'table':dict(), 'current_displacement':0}
        self.scopes = [self.current_scope]
        self.id_counter = 0
        self.temp_count = 0
        self.temp_to_name_map = dict()
        self.call_type = None
        self.calling_func = []
    
    # Visit a parse tree produced by yaplParser#yapl_src.
    def visitYapl_src(self, ctx:yaplParser.Yapl_srcContext):
        res = self.visitChildren(ctx)
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
        for i in SUPPORTED[res[1][1]]:
            if (i[0] == res[0][1] and 
                i[1] == res[2][1]):
                return (True, i[2])
        err_str = (f'Cannot assign objects of type {res[2][1]} '
                f'to {res[0][1]} : {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            for i in res:
                if not i[0]:
                    return (False, i[1])
        else:
            if not res[0]:
                return (False, res[1])
        for i in SUPPORTED[res[1][1]]:
            if (i[0] == res[0][1] and 
                i[1] == res[2][1]):
                return (True, i[2])
        err_str = (f'Unsupported operation between {res[0][1]} '
                f'and {res[2][1]} for operator {res[1][1]}: {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#bool_operator.
    def visitBool_operator(self, ctx:yaplParser.Bool_operatorContext):
        return (True, ctx.getText())

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
        for i in SUPPORTED[res[1][1]]:
            if (i[0] == res[0][1] and 
                i[1] == res[2][1]):
                return (True, i[2])
        err_str = (f'Unsupported operation between {res[0][1]} '
                f'and {res[2][1]} for operator {res[1][1]}: {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#bool_literal.
    def visitBool_literal(self, ctx:yaplParser.Bool_literalContext):
        self.current_scope['table'][self.name_to_temp(ctx.getText())] = {'type':BOOL, 
                                                'scope':self.current_scope['id'], 
                                                'size':1, 
                                                'displacement':self.getDisplacement(1)}
        return (True, BOOL)


    # Visit a parse tree produced by yaplParser#str_literal.
    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        self.current_scope['table'][self.name_to_temp(ctx.getText())] = {'type':STR, 
                                                'scope':self.current_scope['id'], 
                                                'size':8, 
                                                'displacement':self.getDisplacement(8)}
        return (True, STR)

    # Visit a parse tree produced by yaplParser#int_literal.
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        self.current_scope['table'][self.name_to_temp(ctx.getText())] = {'type':INT, 
                                        'scope':self.current_scope['id'], 
                                        'size':4, 
                                        'displacement':self.getDisplacement(4)}
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
        txt = ctx.getText()
        new_id = self.name_to_temp(txt)
        for i in self.scopes:#TODO  check it it is accesible
            if new_id in i['table']:
                return (True, i['table'][new_id]['type'])
        err_msg = f'{bcolors.FAIL}Cannot assign to variable "{txt}" because it is not declared!{bcolors.ENDC}'
        print(err_msg)
        return (False, err_msg)

    def name_to_temp(self, name):
        for t, n in self.temp_to_name_map.items():
            if n == name:
                return t
        new_temp = f't{self.temp_count}'
        self.temp_count +=1
        self.temp_to_name_map[new_temp] = name
        return new_temp

    # Visit a parse tree produced by yaplParser#mem_name.
    def visitMem_name(self, ctx:yaplParser.Mem_nameContext):
        return (True, ctx.getText())

    def getDisplacement(self, size):
        current = self.current_scope['current_displacement']
        self.current_scope['current_displacement']+=size
        return current

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


        # type, scope, size, displacement
        self.current_scope['table'][self.name_to_temp(res[0][1])] = {'type':res[1][1], 
                                                        'scope':self.current_scope['id'], 
                                                        'size':res[1][2], 
                                                        'displacement':self.getDisplacement(res[1][2])}

        return (True, res[1][1]) 
    

    # Visit a parse tree produced by yaplParser#canon_type.
    def visitCanon_type(self, ctx:yaplParser.Canon_typeContext):
        txt = ctx.getText()
        if txt == 'Int':
            return (True, INT, 4)
        if txt == 'String':
            return (True, STR, 8)
        if txt == 'Bool':
            return (True, BOOL, 1)
        if txt == 'IO':
            return (True, IO, 8)
        if txt == 'Object':
            return (True, OBJ, 8)
        if txt == 'SELF_TYPE':
            return (True, self.class_name, 8)
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#scope_def.
    def visitScope_def(self, ctx:yaplParser.Scope_defContext):
        #current_scope += 1
        res = self.visitChildren(ctx)
        #self.cur_dis = 0
        #current_scope -= 1
        if type(res) == list:
            return res[-1]
        return res
    
    # Visit a parse tree produced by yaplParser#bool_expr.
    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        if res[1] in CAN_BE_BOOL:
            return (True, BOOL)
        else:
            err_str = f'{bcolors.FAIL}Expected {ctx.getText()} to be a valid boolean expression {bcolors.ENDC}'
            print(err_str)
            return (False, err_str)
    
    # Visit a parse tree produced by yaplParser#inherited_type_def.
    def visitInherited_type_def(self, ctx:yaplParser.Inherited_type_defContext):
        res = self.visitChildren(ctx)
        TYPE_TABLE[res[0][1]]['parent'] = res[1][1]
        
        return res[0]

    def visitType_def(self, ctx:yaplParser.Type_defContext):
        type_name = ctx.getText()[5::]
        TYPE_TABLE[type_name] = {'parent':OBJ}
        TYPE_TABLE[type_name]['functions'] = dict()
        TYPE_TABLE[type_name]['size'] = 8
        self.class_name = type_name
        self.current_scope['table'][self.name_to_temp('self')] = {'type':type_name, 
                                                        'scope':self.current_scope['id'], 
                                                        'size':8, 
                                                        'displacement':self.getDisplacement(8)}
        SUPPORTED[ASIG].append([type_name, type_name, type_name])
        return (True, type_name)
    
    def visitValid_inheritance(self, ctx:yaplParser.Valid_inheritanceContext):
        class_name = ctx.getText()
        if class_name in TYPE_TABLE:
            return (True, class_name)
        err_msg = f'{bcolors.FAIL}Cannot inheret from {class_name} because it was not previosly defined{bcolors.ENDC}'
        print(err_msg)
        return (False, err_msg)
    
    def getScopeId(self):
        self.id_counter+=1
        return self.id_counter

    # Visit a parse tree produced by yaplParser#func_dec.
    def visitFunc_dec(self, ctx:yaplParser.Func_decContext):
        func_name = ctx.getText().split('(')[0]
        func_scope = {'id': self.getScopeId(), 
                        'name': func_name, 
                        'table':dict(),
                        'current_displacement':0}#TODO cambiar al valor que sí es
        self.scopes.append(func_scope)
        self.current_scope = func_scope
        res = self.visitChildren(ctx)
        self.scopes.pop()
        self.current_scope = self.scopes[-1]

        

        return res
    
    # Visit a parse tree produced by yaplParser#func_params.
    def visitFunc_params(self, ctx:yaplParser.Func_paramsContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) != list:
                res = [res]
            for i in res:
                self.current_scope['table'][i['Parname']] = {'type':i['type'],
                                                    'scope':self.current_scope['id'],
                                                    'size':i['size'],
                                                    'displacement':self.getDisplacement(i['size']),}
        par_spec = None
        if res:
            par_spec = [i['type'] for i in res]
        return (True, {'func params':par_spec})

    # Visit a parse tree produced by yaplParser#param_dec.
    def visitParam_dec(self, ctx:yaplParser.Param_decContext):
        res = self.visitChildren(ctx)
        parname = self.name_to_temp(ctx.getText().split(':')[0])
        return ({'Parname': parname, 'type':res[1], 'size':res[2]})

    # Visit a parse tree produced by yaplParser#acs_object.
    def visitAcs_object(self, ctx:yaplParser.Acs_objectContext):
        res = self.visitChildren(ctx)
        #print(self.current_scope['table'])
        #print(ctx.getText())
        #print(self.temp_to_name_map)
        varname = self.name_to_temp(ctx.getText())
        if res:
            if type(res) == list:
                for i in res:
                    if not i[0]:
                        return (False, i[1])
            else:
                if not res[0]:
                    return (False, res[1])       
        
        for i in self.scopes:
            if varname in i['table']:
                return (True, i['table'][varname]['type'])
        err_msg = f"{bcolors.FAIL}Cannot use {ctx.getText()} before it's declared!{bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)
    

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
        ret_t = self.current_scope['ret_type']
        expr_t = res[1]

        ancestor = self.CanImplicitCast(ret_t, expr_t)
        if ancestor:
            return (True, ancestor)

        err_msg = (f"{bcolors.FAIL}Function {self.current_scope['name']} cannot return " 
                f"'{ctx.getText()}' since it yields {res[1]}. Expecting {ret_t} or inheritor {bcolors.ENDC}")
        print(err_msg)
        return (False, err_msg)
    

    # Visit a parse tree produced by yaplParser#sign_dec.
    def visitSign_dec(self, ctx:yaplParser.Sign_decContext):
        res = self.visitChildren(ctx)
        func_name = ctx.getText().split('(')[0]
        self.current_scope['ret_type'] = res[1][1]
        self.current_scope['param_type'] = res[0][1]['func params']
        func_info = {'args_types':res[0][1]['func params'],
                    'ret_t':res[1][1]}
        TYPE_TABLE[self.class_name]['functions'][func_name] = func_info
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
        return (True, OBJ)

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
        ancestor = self.GetCommonAncestor(res[1][1], res[2][1])
        return (True, ancestor)
    
    # Visit a parse tree produced by yaplParser#func_name.
    def visitFunc_name(self, ctx:yaplParser.Func_nameContext):
        func_name = ctx.getText()
        call_namespace = self.class_name
        if self.call_type:
            call_namespace = self.call_type

        #print(f'Searching for {func_name} in {call_namespace}')
        
        if func_name in TYPE_TABLE[call_namespace]['functions']:
            self.calling_func.append(func_name)
            return (True, TYPE_TABLE[call_namespace]['functions'][func_name]['ret_t'])
        call_namespace = TYPE_TABLE[call_namespace]['parent']
        if call_namespace:
            if func_name in TYPE_TABLE[call_namespace]['functions']:
                self.calling_func.append(func_name)
                return (True, TYPE_TABLE[call_namespace]['functions'][func_name]['ret_t'])
        err_msg = f"{bcolors.FAIL}Invalid call to undeclared function: {func_name} {bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)

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
        #self.calling_func.pop()
        self.call_type = None
        if type(res) == list:
            ret_type = res[-1][1]
        else:
            ret_type = res[1]
        return (True, ret_type)
    
    # Visit a parse tree produced by yaplParser#call_params.
    def visitCall_params(self, ctx:yaplParser.Call_paramsContext):
        res = self.visitChildren(ctx)
        if res:
            if type(res) == list:
                arg_types = [i[1] for i in res]
            else:
                arg_types = [res[1]]
        else:
            arg_types = []

        namespace = self.class_name

        if self.call_type:
            namespace = self.call_type

        if len(self.calling_func) < 1:
            return (False, 'Function not annotated')
        calling_func = self.calling_func.pop()

        func_info = None
        while namespace:
            if calling_func in TYPE_TABLE[namespace]['functions']:
                func_info = TYPE_TABLE[namespace]['functions'][calling_func]
                break
            namespace = TYPE_TABLE[namespace]['parent']
        expected_args = None
        if func_info:
            expected_args = func_info['args_types']
            if expected_args == arg_types:
                self.call_type = func_info['ret_t']
                return (True, func_info['ret_t'])
        
        err_msg = f"{bcolors.FAIL}Recieved {arg_types} instead of the expected: {expected_args} in a call to function '{calling_func}'{bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)
    
    # Visit a parse tree produced by yaplParser#left_hand_op.
    def visitLeft_hand_op(self, ctx:yaplParser.Left_hand_opContext):
        return (True, ctx.getText())
    
    # Visit a parse tree produced by yaplParser#left_hand_operation.
    def visitLeft_hand_operation(self, ctx:yaplParser.Left_hand_operationContext):
        res = self.visitChildren(ctx)
        #TODO distinguir entre cada uno para código
        return (True, BOOL)

    # Visit a parse tree produced by yaplParser#record_type.
    def visitRecord_type(self, ctx:yaplParser.Record_typeContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            self.call_type = res[-1][1]
        else:
            self.call_type = res[1]
        return (True, self.call_type)
    
    # Visit a parse tree produced by yaplParser#record_type_bruh.
    def visitRecord_type_bruh(self, ctx:yaplParser.Record_type_bruhContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            self.call_type = res[-1][1]
        else:
            self.call_type = res[1]
        return (True, self.call_type)

    # Visit a parse tree produced by yaplParser#subs_func.
    def visitSubs_func(self, ctx:yaplParser.Subs_funcContext):
        res = self.visitChildren(ctx)
        if type(res) == list:
            self.call_type = res[-1][1]
        else:
            self.call_type = res[1]
        return (True, self.call_type)
    
    # Visit a parse tree produced by yaplParser#new_call.
    def visitNew_call(self, ctx:yaplParser.New_callContext):
        res = self.visitChildren(ctx)
        return res

    # Visit a parse tree produced by yaplParser#mem_asig.
    def visitMem_asig(self, ctx:yaplParser.Mem_asigContext):
        res = self.visitChildren(ctx)
        if res[0][1] == res[1][1]:
            return res[0]
        
        err_msg = f"{bcolors.FAIL}Cannot initialize member of type {res[0][1]} with expression that yields type {res[1][1]}{bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)

    # Visit a parse tree produced by yaplParser#let_stmt.
    def visitLet_stmt(self, ctx:yaplParser.Let_stmtContext):
        res = self.visitChildren(ctx)
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
        # type, scope, size, displacement
        self.current_scope['table'][self.name_to_temp(ctx.getText().split(':')[0])] = {'type':res[0][1], 
                                                        'scope':self.current_scope['id'], 
                                                        'size':res[0][2], 
                                                        'displacement':self.getDisplacement(res[0][2])}
        return res

    # Visit a parse tree produced by yaplParser#user_defined_t.
    def visitUser_defined_t(self, ctx:yaplParser.User_defined_tContext):
        type_name = ctx.getText()
        if type_name in TYPE_TABLE:
            return (True, type_name, TYPE_TABLE[type_name]['size'])
        err_msg = f"{bcolors.FAIL}Invalid use of undeclared type: {type_name}{bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)

del yaplVisitor