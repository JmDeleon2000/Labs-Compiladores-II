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
    |   ID
    ;


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
    : ID ASSIG_OP ID 
    | ID ASSIG_OP literal 
    | ID ASSIG_OP func_call
    | ID ASSIG_OP LPAREN new_op type RPAREN
    ;
literal
    :   str_literal 
    |   int_literal ;
str_literal: STR_LIT ;
int_literal: DIGITS ;
func_call
    :   ID  subs_func+
    |   LPAREN ID RPAREN subs_func+ 
    |   LPAREN new_op type RPAREN subs_func+ 
    ;
new_op: NEW;
NEW
    :   'new'   ;
subs_func
    :   SUBSCRIPT ID LPAREN call_params RPAREN ;

call_params
    :   (( ID  COMA )* ID )*;
BOOLEAN: 'Bool' ;
STR: 'String' ;
OBJ:  'Object' ;
INT: 'int' ;

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