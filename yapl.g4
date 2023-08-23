grammar yapl;		
yapl_src: class_def EOF ;
class_def
    :   (inherited_type_def
    |  type_def) class_body;

WS: [ \t\r\n]+ -> skip;

MULTILINECOMMENT: '(' '*' (.)* '*' ')' -> skip;
COMMENT: '--' (~[\r\n])+ -> skip;

type_def: 'class' user_defined_t;
inherited_type_def: type_def  'inherits' valid_inheritance;
valid_inheritance: type;

class_body
    :    (LBRACKET (mem_dec)* (func_dec)* RBRACKET  EOS)
    |    empty_class_body ;

empty_class_body: LBRACKET RBRACKET  EOS ;

mem_dec 
    :   mem_name ':' type EOS
    |   mem_name ':' mem_asig EOS;
mem_asig: type '<-' expr;
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
    |   'SELF_TYPE'
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
    :   LBRACKET ret_expr? RBRACKET EOS
    ;
ret_expr:
    expr;
if_stmt:
    'if' bool_expr 'then' expr 'else' expr 'fi';
while_loop:
    'while' bool_expr 'loop' expr 'pool';
bool_expr: expr;
expr    
    :   func_call
    |   LPAREN expr RPAREN
    |   if_stmt
    |   while_loop
    |   sub_expr 
    |   new_call
    |   scope_def
    |   assignment
    ;

//TODO let
func_name:
    ID;
func_call
    :   func_name LPAREN call_params RPAREN
    |   acs_object subs_func
    |   LPAREN record_type RPAREN subs_func
    ;
record_type: expr;
sub_expr
    :   acs_object
    |   literal 
    |   arith_operation
    |   bool_operation
    |   left_hand_operation
    ;
left_hand_operation: left_hand_op sub_expr;
bool_operation
    :   literal bool_operator sub_expr
    |   acs_object bool_operator sub_expr
    |   func_call bool_operator sub_expr
    ;
arith_operation
    :   literal arith_operator expr
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
    |   literal
    ;

new_call
    :   NEW type;
NEW
    :   'new'   ;
subs_func
    :   SUBSCRIPT func_name LPAREN call_params RPAREN
    |   SUBSCRIPT func_name LPAREN call_params RPAREN  subs_func;

call_params
    :   ((expr  COMA )*expr )*;

scope_def:
    LBRACKET (expr EOS)+ RBRACKET;
UDT: [A-Z] [a-zA-Z]*;
ID: 
    [a-z] ([A-Za-z0-9_])* ;

STR_LIT: '"' ~('\r' | '\n' | '"')* '"';
DIGITS : [0-9]+ ;
SUBSCRIPT: '.' ;