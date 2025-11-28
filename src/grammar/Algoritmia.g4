grammar Algoritmia;


programa:
    (NL)* procedimiento+ EOF
    ;

procedimiento:
    ID_MAYUS parametros? bloq_inicio instrucciones bloq_fin (NL)*
    ;

// Delimitadores de bloque robustos (MODO ESTRICTO)
bloq_inicio: '|:' (NL)* ;
bloq_fin:    ':|' ;

parametros:
    ID_MINUSCULA+
    ;

instrucciones:
    (instruccion (NL)+ )* // Las instrucciones deben separarse por Enter
    ;

instruccion
    : asignacion
    | lectura
    | escritura   
    | condicional
    | while_stmt
    | llamada_proc
    | reproduccion
    | addlista
    | poplista
    ;

asignacion:
    ID_MINUSCULA ASSIGN expr
    ;

lectura:
    READ ID_MINUSCULA
    ;

escritura:
    WRITE escritura_item+
    ;

escritura_item:
      STRING
    | expr
    ;

reproduccion:
    ( PLAY | PLAY_ALT ) expr
    ;

condicional:
    IF expr bloq_inicio instrucciones bloq_fin
    ( (NL)* ELSE bloq_inicio instrucciones bloq_fin )?
    ;

while_stmt:
    WHILE expr bloq_inicio instrucciones bloq_fin
    ;

llamada_proc:
    ID_MAYUS expr*
    ;

addlista:
    ID_MINUSCULA APPEND expr
    ;

poplista:
    CUT ID_MINUSCULA '[' expr ']'
    ;

expr:
    comparacion
    ;

comparacion:
    aritmetica ( (EQ | NEQ | LT | GT | LE | GE) aritmetica )*
    ;

aritmetica:
    termino ( (PLUS | MINUS) termino )*
    ;

termino:
    factor ( (MULT | DIV | MOD) factor )*
    ;

factor:
      MINUS factor
    | '(' expr ')'
    | INT
    | ID_MINUSCULA
    | ID_MAYUS
    | ID_MINUSCULA '[' expr ']'
    | LEN ID_MINUSCULA
    | lista_literal
    ;

lista_literal:
    '{' elements_list? '}'
    ;

elements_list:
    expr+
    ;


READ:   '<?>';
WRITE:  '<w>';
PLAY:   '(:)';
PLAY_ALT: '<:>';
ASSIGN: '<-';
APPEND: '<<';
CUT:    '8<';
LEN:    '#';

IF:     'if';
ELSE:   'else';
WHILE:  'while';

EQ:     '=';
NEQ:    '/=';
LE:     '<=';
GE:     '>=';
LT:     '<';
GT:     '>';

PLUS:   '+';
MINUS:  '-';
MULT:   '*';
DIV:    '/';
MOD:    '%';

STRING: '"' (~["\r\n] | '\\' .)* '"'; // Asegura que las strings sean solo con comillas
INT:    [0-9]+;

ID_MAYUS:       [A-Z][A-Za-z0-9_]*;
ID_MINUSCULA:   [a-z_][A-Za-z0-9_]*;

WS: [ \t]+ -> skip;
NL: [\r\n]+ ;

COMMENT: '###' .*? '###' -> skip;
