# Generated from yapl.g4 by ANTLR 4.13.0
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


    # Visit a parse tree produced by yaplParser#class_def.
    def visitClass_def(self, ctx:yaplParser.Class_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#type_def.
    def visitType_def(self, ctx:yaplParser.Type_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#inherited_type_def.
    def visitInherited_type_def(self, ctx:yaplParser.Inherited_type_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#class_body.
    def visitClass_body(self, ctx:yaplParser.Class_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#empty_class_body.
    def visitEmpty_class_body(self, ctx:yaplParser.Empty_class_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#mem_dec.
    def visitMem_dec(self, ctx:yaplParser.Mem_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#type.
    def visitType(self, ctx:yaplParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#user_defined_t.
    def visitUser_defined_t(self, ctx:yaplParser.User_defined_tContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_dec.
    def visitFunc_dec(self, ctx:yaplParser.Func_decContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_params.
    def visitFunc_params(self, ctx:yaplParser.Func_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_body.
    def visitFunc_body(self, ctx:yaplParser.Func_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#expr.
    def visitExpr(self, ctx:yaplParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#sub_expr.
    def visitSub_expr(self, ctx:yaplParser.Sub_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#arith_operation.
    def visitArith_operation(self, ctx:yaplParser.Arith_operationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#left_hand_op.
    def visitLeft_hand_op(self, ctx:yaplParser.Left_hand_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#arith_operator.
    def visitArith_operator(self, ctx:yaplParser.Arith_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#plus_op.
    def visitPlus_op(self, ctx:yaplParser.Plus_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#minus_op.
    def visitMinus_op(self, ctx:yaplParser.Minus_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#division_op.
    def visitDivision_op(self, ctx:yaplParser.Division_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#mul_op.
    def visitMul_op(self, ctx:yaplParser.Mul_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#bool_op.
    def visitBool_op(self, ctx:yaplParser.Bool_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#assig_op.
    def visitAssig_op(self, ctx:yaplParser.Assig_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#identifier.
    def visitIdentifier(self, ctx:yaplParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#assignment.
    def visitAssignment(self, ctx:yaplParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#literal.
    def visitLiteral(self, ctx:yaplParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#bool_literal.
    def visitBool_literal(self, ctx:yaplParser.Bool_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#str_literal.
    def visitStr_literal(self, ctx:yaplParser.Str_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#int_literal.
    def visitInt_literal(self, ctx:yaplParser.Int_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#acs_object.
    def visitAcs_object(self, ctx:yaplParser.Acs_objectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#func_call.
    def visitFunc_call(self, ctx:yaplParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#new_op.
    def visitNew_op(self, ctx:yaplParser.New_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#subs_func.
    def visitSubs_func(self, ctx:yaplParser.Subs_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#call_params.
    def visitCall_params(self, ctx:yaplParser.Call_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by yaplParser#canon_type.
    def visitCanon_type(self, ctx:yaplParser.Canon_typeContext):
        return self.visitChildren(ctx)



del yaplParser