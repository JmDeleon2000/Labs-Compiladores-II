grammar Expr;		
prog:	expr EOF ;
expr:	expr ('*'|'/') expr
    |	expr ('+'|'-') expr
    |	INT
    |	'(' expr ')'
    |   ID
    ;
NEWLINE : [\r\n]+ -> skip;
INT     : [0-9]+ ;
ID: 
    [a-z] ([A-Za-z0-9_])* ;