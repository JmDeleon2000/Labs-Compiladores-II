grammar yapl;		
yapl_src: class_def EOF ;
class_def
    :   (inherited_type_def
    |  type_def) class_body;

WS: [ \t\r\n]+ -> skip;

type_def: 'class' user_defined_t;
inherited_type_def: 'class'  user_defined_t  'inherits' type;

class_body
    :    (LBRACKET (mem_dec | func_dec)+ RBRACKET  EOS)
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
type
    :   canon_type
    |   user_defined_t
    ;


func_dec:
    ID LPAREN func_params RPAREN ':' type func_body;

func_params
    :   (( ID ':' type  COMA )* ID ':' type )?;
func_body
    :   LBRACKET  RBRACKET EOS
    |   LBRACKET  expr+  RBRACKET EOS
    ;
expr    
    :   sub_expr EOS    
    |   'if' bool_expr 'then' expr 'else' expr 'fi'
    |   'while' bool_expr 'loop' expr 'pool' 
    |   scope_def
    ;
bool_expr: sub_expr;
scope_def:
    LBRACKET expr RBRACKET;
//TODO let
sub_expr
    :   func_call
    |   assignment
    |   acs_object
    |   literal 
    |   arith_operation
    |   left_hand_op sub_expr
    |   LBRACKET sub_expr RBRACKET
    |   bool_op sub_expr
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
bool_op
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
    :   LPAREN acs_object RPAREN
    |   ID
    |   new_op type
    |   literal
    ;
func_call
    :   acs_object  subs_func+
    ;
new_op: NEW;
NEW
    :   'new'   ;
subs_func
    :   SUBSCRIPT ID LPAREN call_params RPAREN ;

call_params
    :   (( acs_object  COMA )* acs_object )*;
BOOLEAN: 'Bool' ;
STR:    'String' ;
OBJ:    'Object' ;
INT:    'Int' ;

canon_type
    :    BOOLEAN
    |   STR
    |   INT
    |   OBJ
    ;

user_defined_t
    :   UDT ; 

UDT: [A-Z] [a-zA-Z]*;
ID: 
    [a-z] ([A-Za-z0-9_])* ;

STR_LIT: '"' [a-zA-Z _]* '"';
DIGITS : [0-9]+ ;
SUBSCRIPT: '.' ;