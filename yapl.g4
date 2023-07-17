grammar yapl;		
yapl_src: class_def EOF ;
class_def
    :   (inherited_type_def
    |  type_def) class_body;

WS: [ \t\r\n]+ -> skip;

type_def: 'class' ID;
inherited_type_def: 'class'  ID  'inherits' ID;

class_body
    :    (LBRACKET (mem_dec | func_dec)+ RBRACKET  EOS)
    |    empty_class_body ;

empty_class_body: LBRACKET RBRACKET  EOS ;

mem_dec: 
    ID ':' type EOS;

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

user_defined_t
    :   UDT ; 

UDT: [A-Z] [a-zA-Z]*;

func_dec:
    ID LPAREN func_params RPAREN ':' type func_body;

func_params
    :   (( ID ':' type  COMA )* ID ':' type )*;
func_body
    :   LBRACKET  RBRACKET 
    |   LBRACKET  expr+  RBRACKET 
    ;
expr    :   sub_expr EOS    ;
sub_expr
    :   func_call
    |   assignment
    |   acs_object
    |   literal 
    |   literal operator sub_expr
    |   acs_object operator sub_expr
    |   func_call operator sub_expr
    |   left_hand_op sub_expr
    ;
left_hand_op
    :   'isvoid'
    |   '~'
    |   'not'
    ;
operator
    :   arith_op
    |   bool_op
    ;
arith_op
    :   '+'
    |   '-'
    |   '/'
    |   '*'
    ;
bool_op
    :   '<'
    |   '<='
    |   '='
    ;
assignment
    : ID ASSIG_OP sub_expr
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

ID: 
    [a-z] ([A-Za-z0-9_])* ;
STR_LIT: '"' [a-zA-Z _]+ '"';
DIGITS : [0-9]+ ;
SUBSCRIPT: '.' ;