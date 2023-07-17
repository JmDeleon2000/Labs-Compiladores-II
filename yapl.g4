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
    |   LBRACKET  statement+  RBRACKET 
    ;
statement
    :   func_call EOS
    |   assignment EOS
    ;
assignment
    : ID ASSIG_OP acs_object
    | ID ASSIG_OP literal 
    | ID ASSIG_OP func_call
    ;
literal
    :   str_literal 
    |   int_literal ;
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