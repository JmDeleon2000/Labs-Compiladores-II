grammar yapl;		
yapl_src: class_def EOF ;
class_def
    :   (inherited_type_def
    |  type_def) class_body;

WS: [ \t\r\n]+ -> skip;

type_def: 'class' user_defined_t;
inherited_type_def: type_def  'inherits' valid_inheritance;
valid_inheritance: type;

class_body
    :    (LBRACKET (mem_dec)* (func_dec)* RBRACKET  EOS)
    |    empty_class_body ;

empty_class_body: LBRACKET RBRACKET  EOS ;

mem_dec: 
    mem_name ':' type EOS;

mem_name:
    ID;

LBRACKET: '{';
RBRACKET: '}';
LPAREN: '(' ;
RPAREN: ')' ;
EOS: ';' ;
ASSIG_OP: '<-' ;
THIS_PTR   : 'SELF_TYPE' ;
COMA: ',' ;

canon_type
    :   'Bool' 
    |   'String'
    |   'Object'
    |   'Int'
    ;

ret_type:
    type;
user_defined_t
    :   UDT ; 
type
    :   canon_type
    |   user_defined_t
    ;

sign_dec: ID LPAREN func_params RPAREN ':' ret_type;
func_dec:
    sign_dec func_body;
param_dec:
    ID ':' type;

func_params
    :   (( param_dec  COMA )* param_dec )?;
func_body
    :   LBRACKET  RBRACKET EOS
    |   LBRACKET  (expr EOS)* ret_expr  RBRACKET EOS
    ;
ret_expr:
    expr;
expr    
    :   'if' bool_expr 'then' expr 'else' expr 'fi'
    |   'while' bool_expr 'loop' expr 'pool' 
    |   scope_def
    |   sub_expr 
    ;
bool_expr: sub_expr;
scope_def:
    LBRACKET expr RBRACKET;
//TODO let
sub_expr
    :   acs_object
    |   assignment
    |   func_call
    |   literal 
    |   arith_operation
    |   bool_operation
    |   left_hand_op sub_expr
    |   LPAREN sub_expr RPAREN
    ;
bool_operation
    :   literal bool_operator sub_expr
    |   acs_object bool_operator sub_expr
    |   func_call bool_operator sub_expr
    ;
arith_operation
    :   literal arith_operator sub_expr
    |   acs_object arith_operator sub_expr
    |   func_call arith_operator sub_expr
    ;
left_hand_op
    :   'isvoid'
    |   '~'
    |   'not'
    ;
arith_operator
    :   plus_op
    |   minus_op
    |   division_op
    |   mul_op
    ;
plus_op
    :   '+'
    ;
minus_op
    :   '-'
    ;
division_op
    :   '/'
    ;
mul_op
    :   '*'
    ;
bool_operator
    :   '<'
    |   '<='
    |   '='
    ;
assig_op
    :   ASSIG_OP
    ;
identifier
    :   ID
    ;
assignment
    : identifier assig_op sub_expr
    ;
literal
    :   str_literal 
    |   int_literal 
    |   bool_literal ;
bool_literal
    :   'true'
    |   'false' ; 
str_literal: STR_LIT ;
int_literal: DIGITS ;
acs_object
    :   ID
    |   new_op type
    |   literal
    ;
func_call
    :   ID LPAREN call_params RPAREN
    |   acs_object  subs_func+
    ;
new_op: NEW;
NEW
    :   'new'   ;
subs_func
    :   SUBSCRIPT ID LPAREN call_params RPAREN ;

call_params
    :   ((sub_expr  COMA )*sub_expr )*;


UDT: [A-Z] [a-zA-Z]*;
ID: 
    [a-z] ([A-Za-z0-9_])* ;

STR_LIT: '"' [a-zA-Z _,.]* '"';
DIGITS : [0-9]+ ;
SUBSCRIPT: '.' ;