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

IO = 'IO'
OBJ = 'Object'
ERR = 'error'
INT = 'int'
PLUS = '+'
MUL = '*'
DIV = '/'
MIN = '-'
ASIG = '<-'
BOOL = 'bool'
STR = 'string'
SUPPORTED = {
    PLUS:[(INT, INT, INT),],
    DIV:[(INT, INT, INT),],
    MUL:[(INT, INT, INT),],
    MIN:[(INT, INT, INT),],
    ASIG:[(INT, INT, INT),
          (STR, STR, STR),
          (BOOL, BOOL, BOOL),],
}
CAN_BE_BOOL = [BOOL, INT, ]

VALID_TYPES = [IO, BOOL, STR, INT, ]


class yaplVisImpl(yaplVisitor):    

    def __init__(self):
        self.current_scope = {'id': 0, 'name': 'global', 'table':dict(), 'current_displacement':0}
        self.scopes = [self.current_scope]
        self.id_counter = 0
    
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
                return (True, i[2])
        err_str = (f'Cannot assign objects of type {result[2][1]} '
                f'to {result[0][1]} : {ctx.getText()}')
        err_str = f'{bcolors.FAIL}{err_str}{bcolors.ENDC}'
        print(err_str)
        return (False, ERR)

    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        result = self.visitChildren(ctx)
        print(result)
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
        txt = ctx.getText()
        new_id = hash(txt)
        for i in self.scopes:#TODO  check it it is accesible
            if new_id in i['table']:
                return (True, i['table'][hash(txt)]['type'])
        err_msg = f'{bcolors.FAIL}Cannot assign to variable "{txt}" because it is not declared!{bcolors.ENDC}'
        print(err_msg)
        return (False, err_msg)



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
        
        # type, scope, size, displacement
        self.current_scope['table'][hash(res[0][1])] = {'type':res[1][1], 
                                                        'scope':self.current_scope['id'], 
                                                        'size':res[1][2], 
                                                        'displacement':self.getDisplacement(res[1][2])}

        #print(self.scopes[self.current_scope])
        return (True, 'Member declaration') 
    

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
        return (False, ERR)

    # Visit a parse tree produced by yaplParser#scope_def.
    def visitScope_def(self, ctx:yaplParser.Scope_defContext):
        current_scope += 1
        result = self.visitChildren(ctx)
        self.cur_dis = 0
        current_scope -= 1
        return result
    
    # Visit a parse tree produced by yaplParser#bool_expr.
    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        if res[1] in CAN_BE_BOOL:
            return (True, BOOL)
        else:
            err_str = f'{bcolors.FAIL}Expected {ctx.getText()} to be a valid boolean expression {bcolors.ENDC}'
            print(err_str)
            return (False, err_str)
    

    def visitType_def(self, ctx:yaplParser.Type_defContext):
        VALID_TYPES.append(ctx.getText()[5::])
        return (True, 'Foo')
    
    def visitValid_inheritance(self, ctx:yaplParser.Valid_inheritanceContext):
        class_name = ctx.getText()
        if class_name in VALID_TYPES:
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
                        'current_displacement':0}
        self.scopes.append(func_scope)
        self.current_scope = func_scope
        res = self.visitChildren(ctx)
        
        return res
    
    # Visit a parse tree produced by yaplParser#func_params.
    def visitFunc_params(self, ctx:yaplParser.Func_paramsContext):
        res = self.visitChildren(ctx)
        if res:
            for i in res:
                self.current_scope['table'][i['Parname']] = {'type':i['type'],
                                                    'scope':self.current_scope['id'],
                                                    'size':i['size'],
                                                    'displacement':self.getDisplacement(i['size'])}

        return (True, '')

    # Visit a parse tree produced by yaplParser#param_dec.
    def visitParam_dec(self, ctx:yaplParser.Param_decContext):
        res = self.visitChildren(ctx)
        parname, partype = ctx.getText().split(':') 
        return ({'Parname': parname, 'type':res[1], 'size':res[2]})

    # Visit a parse tree produced by yaplParser#acs_object.
    def visitAcs_object(self, ctx:yaplParser.Acs_objectContext):
        varname = ctx.getText()
        for i in self.scopes:
            if varname in i['table']:
                return (True, i['table'][varname]['type'])
        err_msg = f"{bcolors.FAIL}Cannot use {varname} before it's declared!{bcolors.ENDC}"
        print(err_msg)
        return (False, err_msg)

del yaplVisitor