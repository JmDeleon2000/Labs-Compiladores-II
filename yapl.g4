grammar yapl;


COMMENT: START_COMMENT .*? END_COMMENT -> skip;
LINE_COMMENT: '--' .*? '\n' -> skip;
WS: [ \t\r\n\f]+ -> skip;

yapl_src: (class_grammar ';')+;
class_grammar: (inherited_type_def | type_def) '{' (feature ';')* '}';
feature: func_dec
| mem_dec;
formal: mem_name ':' type;
expr
: '(' expr ')' # paren
| expr('@'called_type)? mark_last_t func_name '(' (expr (',' expr)*)? ')' # bigexpr
| free_func_name '(' ((expr  ',' )*expr )* ')' # func_call
| IF bool_expr then expr else expr FI # if_stmt
| WHILE bool_expr LOOP expr POOL # while_loop
| '{' (expr eos)+ '}' # comp_expr
| let_stmt # let
| NEW type # new_call
| '~' expr # negation
| ISVOID expr # isvoid
| expr division_op expr # arith_operation
| expr mul_op expr # arith_operation
| expr plus_op expr # arith_operation
| expr minus_op expr # arith_operation
| expr (lt | leq | eq) expr # bool_operation
| NOT expr # not
| ID # identifier
| INT # int_literal
| STRING # str_literal
| TRUE # bool_literal
| FALSE # bool_literal
| var_name ASSIGN_OP expr # assignment; 
eos: ';';
lt: LESS_THAN;
leq: LESS_EQUAL;
eq: EQUAL;
mark_last_t: '.';
var_name: ID;
free_func_name: func_name;
then: THEN;
else: ELSE;

let_stmt
    :   'let' let_type_dec 'in' expr;
let_type_dec:   mem_name ':' type ('<-' expr)?    ;

subs_func: '.' func_name '(' ((call_param  ',' )*call_param )* ')';
call_param: expr;
type_def: CLASS user_defined_t;
inherited_type_def: type_def  'inherits' valid_inheritance;
valid_inheritance: type;
user_defined_t: type;

called_type: type;

mul_op:    MULT;
division_op:    DIV;
plus_op:   PLUS;
minus_op:  MINUS;

bool_expr:
    expr;
sign_dec: new_func_name '(' func_params ')' ':' ret_type;
new_func_name: ID;
func_dec:
    sign_dec func_body;
func_body:   '{' ret_expr? '}' ;
mem_dec:  mem_name ':' type (ASSIGN_OP expr)?;

mem_name: ID;
type: TYPE;
func_params:   (( func_param  ',' )* func_param )?;
func_param: formal;
ret_type:   type;
ret_expr: expr;
func_name:  ID;


//reserved keywords case insensitive
CLASS: [Cc][Ll][Aa][Ss][Ss];
INHERITS: [Ii][Nn][Hh][Ee][Rr][Ii][Tt][Ss];
ELSE: [Ee][Ll][Ss][Ee];
IF: [Ii][Ff];
THEN: [Tt][Hh][Ee][Nn];
FI: [Ff][Ii];
LOOP: [Ll][Oo][Oo][Pp];
POOL: [Pp][Oo][Oo][Ll];
IN: [Ii][Nn];
ISVOID: [Ii][Ss][Vv][Oo][Ii][Dd];
WHILE: [Ww][Hh][Ii][Ll][Ee];
NEW: [Nn][Ee][Ww];
NOT: [Nn][Oo][Tt];
LET: [Ll][Ee][Tt];
//reserved keywords case sensitive
TRUE: 'true';
FALSE: 'false';

STRING: '"'  .*?  '"' ;

//Other types
ASSIGN_OP: '<-';
ID: [a-z][_a-zA-Z0-9]*; //start with minuscule letter
TYPE: [A-Z][_a-zA-Z0-9]*; //start with mayus letter
INT: [-]?[0-9]+;
START_COMMENT: '(*';
END_COMMENT: '*)';

PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
EQUAL: '=';
LESS_THAN: '<';
LESS_EQUAL: '<=';



