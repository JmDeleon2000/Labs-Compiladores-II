# Generated from yapl.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .yaplParser import yaplParser
else:
    from yaplParser import yaplParser

# This class defines a complete generic visitor for a parse tree produced by yaplParser.

class yaplVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by yaplParser#yapl_src.
    def visitYapl_src(self, ctx:yaplParser.Yapl_srcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#class_grammar.
    def visitClass_grammar(self, ctx:yaplParser.Class_grammarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#feature.
    def visitFeature(self, ctx:yaplParser.FeatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#formal.
    def visitFormal(self, ctx:yaplParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#identifier.
    def visitIdentifier(self, ctx:yaplParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#negation.
    def visitNegation(self, ctx:yaplParser.NegationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#while_loop.
    def visitWhile_loop(self, ctx:yaplParser.While_loopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#isvoid.
    def visitIsvoid(self, ctx:yaplParser.IsvoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#assignment.
    def visitAssignment(self, ctx:yaplParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#bool_operation.
    def visitBool_operation(self, ctx:yaplParser.Bool_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#if_stmt.
    def visitIf_stmt(self, ctx:yaplParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#bool_literal.
    def visitBool_literal(self, ctx:yaplParser.Bool_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_call.
    def visitFunc_call(self, ctx:yaplParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#new_call.
    def visitNew_call(self, ctx:yaplParser.New_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#str_literal.
    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#int_literal.
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#paren.
    def visitParen(self, ctx:yaplParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#not.
    def visitNot(self, ctx:yaplParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#scope_def.
    def visitScope_def(self, ctx:yaplParser.Scope_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#let.
    def visitLet(self, ctx:yaplParser.LetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#arith_operation.
    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#bigexpr.
    def visitBigexpr(self, ctx:yaplParser.BigexprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#lt.
    def visitLt(self, ctx:yaplParser.LtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#leq.
    def visitLeq(self, ctx:yaplParser.LeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#eq.
    def visitEq(self, ctx:yaplParser.EqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#var_name.
    def visitVar_name(self, ctx:yaplParser.Var_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#let_stmt.
    def visitLet_stmt(self, ctx:yaplParser.Let_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#let_type_dec.
    def visitLet_type_dec(self, ctx:yaplParser.Let_type_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#subs_func.
    def visitSubs_func(self, ctx:yaplParser.Subs_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#call_param.
    def visitCall_param(self, ctx:yaplParser.Call_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#type_def.
    def visitType_def(self, ctx:yaplParser.Type_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#inherited_type_def.
    def visitInherited_type_def(self, ctx:yaplParser.Inherited_type_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#valid_inheritance.
    def visitValid_inheritance(self, ctx:yaplParser.Valid_inheritanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#user_defined_t.
    def visitUser_defined_t(self, ctx:yaplParser.User_defined_tContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#called_type.
    def visitCalled_type(self, ctx:yaplParser.Called_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#mul_op.
    def visitMul_op(self, ctx:yaplParser.Mul_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#division_op.
    def visitDivision_op(self, ctx:yaplParser.Division_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#plus_op.
    def visitPlus_op(self, ctx:yaplParser.Plus_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#minus_op.
    def visitMinus_op(self, ctx:yaplParser.Minus_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#bool_expr.
    def visitBool_expr(self, ctx:yaplParser.Bool_exprContext):
        res = self.visitChildren(ctx)
        print('asdfdsf')
        print(f' bool: {res}')
        return res


    # Visit a parse tree produced by yaplParser#sign_dec.
    def visitSign_dec(self, ctx:yaplParser.Sign_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#new_func_name.
    def visitNew_func_name(self, ctx:yaplParser.New_func_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_dec.
    def visitFunc_dec(self, ctx:yaplParser.Func_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_body.
    def visitFunc_body(self, ctx:yaplParser.Func_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#mem_dec.
    def visitMem_dec(self, ctx:yaplParser.Mem_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#mem_name.
    def visitMem_name(self, ctx:yaplParser.Mem_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#type.
    def visitType(self, ctx:yaplParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_params.
    def visitFunc_params(self, ctx:yaplParser.Func_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_param.
    def visitFunc_param(self, ctx:yaplParser.Func_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#ret_type.
    def visitRet_type(self, ctx:yaplParser.Ret_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#ret_expr.
    def visitRet_expr(self, ctx:yaplParser.Ret_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_name.
    def visitFunc_name(self, ctx:yaplParser.Func_nameContext):
        return self.visitChildren(ctx)



del yaplParser