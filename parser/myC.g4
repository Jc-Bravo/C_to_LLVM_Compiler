grammar myC;

prog :(include)* (initialBlock|arrayInitBlock|structInitBlock|mStructDef|mFunction)*;

include : '#include' '<' mLIB '>';

mStructDef : mStruct '{' (structParam)+ '}'';';

structParam : (mType|mStruct) (mID|mArray) (',' (mID|mArray))* ';';

mFunction : (mType|mVoid|mStruct) mID '(' params ')' '{' funcBody '}';

params : param (','param)* |;
param : mType mID;

funcBody : body returnBlock;

body : (block | func';')*;

block : initialBlock | arrayInitBlock | structInitBlock | assignBlock | ifBlocks | whileBlock | forBlock | returnBlock;

initialBlock : (mType) mID ('=' expr)? (',' mID ('=' expr)?)* ';';
arrayInitBlock : mType mID '[' mINT ']'';'; 
structInitBlock : mStruct (mID|mArray)';';


assignBlock : ((arrayItem|mID|structMember) '=')+  expr ';';


ifBlocks : ifBlock (elifBlock)* (elseBlock)?;
ifBlock : 'if' '('condition')' '{' body '}';
elifBlock : 'else' 'if' '(' condition ')' '{' body '}';
elseBlock : 'else' '{' body '}';

condition :  expr;

whileBlock : 'while' '(' condition ')' '{' body '}';

forBlock : 'for' '(' for1Block  ';' condition ';' for3Block ')' ('{' body '}'|';');
for1Block :  mID '=' expr (',' for1Block)?|;
for3Block : mID '=' expr (',' for3Block)?|;

returnBlock : 'return' (mINT|mID)? ';';

expr
    : '(' expr ')'               #parens
    | op='!' expr                   #Neg
    | expr op=('*' | '/' | '%') expr   #MulDiv 
    | expr op=('+' | '-') expr   #AddSub
    | expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') expr #Judge
    | expr '&&' expr             # AND
    | expr '||' expr             # OR
    | arrayItem                  #arrayitem
    | structMember               #structmember
    | (op='-')? mINT             #int                          
    | (op='-')? mDOUBLE          #double
    | mCHAR                       #char
    | mSTRING                     #string             
    | mID                         #identifier   
    | func                       #function                                     
    ;

mType : 'int'| 'double'| 'char'| 'string';

mArray : mID '[' mINT ']'; 

mVoid : 'void';

mStruct : 'struct' mID;

structMember: (mID | arrayItem)'.'(mID | arrayItem);

arrayItem : mID '[' expr ']';


func : (strlenFunc | atoiFunc | printfFunc | scanfFunc | getsFunc | selfDefinedFunc);

strlenFunc : 'strlen' '(' mID ')';

atoiFunc : 'atoi' '(' mID ')' ;

printfFunc 
    : 'printf' '(' (mSTRING | mID) (','expr)* ')';

scanfFunc : 'scanf' '(' mSTRING (','('&')?(mID|arrayItem|structMember))* ')';

getsFunc : 'gets' '(' mID ')';

selfDefinedFunc : mID '('((argument|mID)(','(argument|mID))*)? ')';

argument : mINT | mDOUBLE | mCHAR | mSTRING;

mID : ID;

mINT : INT;

mDOUBLE : DOUBLE;

mCHAR : CHAR;

mSTRING : STRING;

mLIB : LIB;


ID : [a-zA-Z_][0-9A-Za-z_]*;

INT : [0-9]+;

DOUBLE : [0-9]+'.'[0-9]+;

CHAR : '\''.'\'';

STRING : '"'.*?'"';


LIB : [a-zA-Z]+'.h'?;

Conjunction : '&&' | '||';

Operator : '!' | '+' | '-' | '*' | '/' | '==' | '!=' | '<' | '<=' | '>' | '>=';

LineComment: '//'.*?'\r'?'\n'   -> skip;

BlockComment:  '/*'.*?'*/'  -> skip;

WS : [ \t\r\n]+ -> skip ; 

