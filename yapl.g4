grammar yapl;		
yapl_src: class_def EOF ;
class_def: (type_def|inherint_type_def) CLASS_BODY;


type_def:   CLASS WS ID;
inherint_type_def:   CLASS WS ID WS INHERITS ID;
INHERITS: 'inherits';
ID: 
    [a-z] ([A-Za-z0-9_])* ;
CLASS: 'class' ;
LBRACKET: '{';
RBRACKET: '}';
LPAREN: '(' ;
RPAREN: ')' ;
EOS: ';' ;
WS : ' '+ -> skip;
NEWLINE : [\r\n]+ -> skip;
DIGITS     : [0-9]+ ;
ASSIG_OP: '<-' ;
THIS_PTR   : 'SELF_TYPE' ;
fragment MHWS: [ \r\n\t]* ;
COMA: ',' ;
TYPE: 
    ID
    |   CANON_TYPE
    ;
MEM_DEC: 
    ID ' '* ':' ' '* TYPE;
fragment PARAM_DEC
    :   ((MEM_DEC COMA WS)* MEM_DEC)*;
FUNC_DEC:
    ID LPAREN PARAM_DEC RPAREN ':' TYPE MHWS FUNC_BODY;
CLASS_BODY
    :  MHWS  LBRACKET MHWS  ( ((MEM_DEC EOS)|FUNC_DEC) MHWS )+ MHWS  RBRACKET MHWS  EOS;

FUNC_BODY
    :   LBRACKET MHWS RBRACKET 
    |   LBRACKET MHWS SATEMENT+ MHWS RBRACKET 
    ;

SUBSCRIPT: '.' ;
SATEMENT
    :   ID SUBSCRIPT ID LPAREN CALL_PARAMS RPAREN EOS
    ;
fragment CALL_PARAMS
    :   ((MHWS ID MHWS COMA MHWS)* ID MHWS)*;
BOOLEAN: 'Bool' ;
STR: 'String' ;
OBJ:  'Object' ;
INT: 'int' ;

CANON_TYPE
    :    BOOLEAN
    |   STR
    |   INT
    |   OBJ
    ;