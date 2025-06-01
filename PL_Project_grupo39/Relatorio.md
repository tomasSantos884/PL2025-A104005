# Relatório do Projeto: Compilador para Pascal Standard

## UC de Processamento de Linguagens

### Data: 01/06/2025

### Realizado por

- **Gabriel Torres** (104169)
- **Tomás Santos** (A104005)
- **Tomás Silva** (A104362)

**Grupo 39**


## Sumário

- Introdução
- Gramática
- [Lexer (lexer.py)](#lexer-lexerpy)
- [Parser/Yacc (yaccer.py)](#parser-yacc-yaccerpy)
- Exemplos de Entrada e Saída
- Conclusão

---

## Introdução

Este projeto implementa um **analisador léxico** e **sintático** para uma linguagem baseada no Pascal Standard, utilizando a biblioteca PLY (Python Lex-Yacc). O objetivo é ler programas em Pascal, analisar sua estrutura e gerar código para uma VM da Unidade Curricular.

---

## Gramática

A GIC utilizada cobre os principais elementos do Pascal, incluindo:

- Declaração de variáveis (simples e arrays)
- Blocos de código (`begin ... end`)
- Estruturas de controle: `if`, `while`, `for`
- Comandos de entrada e saída: `readln`, `write`, `writeln`
- Expressões aritméticas e booleanas


```text
Program : Header SEMICOLON Block DOT

Header  : PROGRAM identifier

Block   : Var_declaration_block Code_block

Var_declaration_block : VAR Var_list
	|

Var_list : Var_declaration Var_list
	| Var_declaration

Var_declaration : Identifier_list COLON Type SEMICOLON

Identifier_list : identifier COMMA Identifier_list
    | identifier

Type : TINTEGER
    | TREAL
    | TSTRING
    | TCHAR
    | TBOOLEAN
    | Array_type
    
Array_type : ARRAY LBRACKET integer DOTDOT integer RBRACKET OF Type

Code_block : BEGIN Statements END

Statements : Statement SEMICOLON Statements
	| Statement
 
Statement : Assignment_statement
	| Code_block
	| If_statement
	| While_statement
	| For_statement
    | Write_statement
    | Readln_statement
	|

If_statement : IF Expression THEN Statement ELSE Statement
	| IF Expression THEN Statement

While_statement : WHILE Expression DO Statement

For_statement : FOR assignment_statement TO Expression DO Statement
	| FOR assignment_statement DOWNTO Expression DO Statement
 
Write_statement : WRITE LPAREN Param_list RPAREN 
    | WRITELN LPAREN Param_list RPAREN 

Param_list : Param_list COMMA Param
    | Param

Param : Expression

Readln_statement : READLN LPAREN identifier RPAREN
                | READLN LPAREN identifier LBRACKET Expression RBRACKET RPAREN
 
Assignment_statement : identifier ASSIGNMENT Expression
                     | identifier LBRACKET Expression RBRACKET ASSIGNMENT Expression

Expression : Expression And_or Expression_m
	| Expression_m

Expression_m : Expression_s
	| Expression_m Sign Expression_s
 
Expression_s : Element 
	| Expression_s Psign Element

And_or : AND
	| OR
	
Psign : TIMES
	| DIVISION

Sign : PLUS
	| MINUS
	| DIV
	| MOD
	| EQ
	| NEQ
	| LT
	| LTE
	| GT
	| GTE

Element : identifier
    | identifier LBRACKET Expression RBRACKET
	| real
	| integer
	| string
	| char
    | boolean
	| LPAREN Expression RPAREN
	| NOT Element
 
identifier : IDENTIFIER
real : REAL
integer : INTEGER
string : STRING
char : CHAR
boolean : BOOLEAN
```


---

## Lexer (lexer.py)


---

## Lexer (lexer.py)

O **lexer** é responsável por identificar os tokens do código fonte Pascal. A lista completa de tokens reconhecidos é:

```python
tokens = (
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    
    'WRITE',
    'WRITELN',
    'READLN',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'DO',
    'FOR',
    'TO',
    'DOWNTO',
    
    'INTEGER',
    'REAL',
    'STRING',
    'CHAR',
    'BOOLEAN',
    
    'TINTEGER',
    'TREAL',
    'TSTRING',
    'TCHAR',
    'TBOOLEAN',
    
    'IDENTIFIER',
    
    'ASSIGNMENT',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'DOT',
    'LPAREN',
    'RPAREN',
    
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVISION',
    'DIV',
    'MOD',
    'EQ',
    'NEQ',
    'LT',
    'LTE',
    'GT',
    'GTE',
    
    'NOT',
    'AND',
    'OR',
    
    'ARRAY',
    'LBRACKET',
    'RBRACKET',
    'DOTDOT',
    'OF',
    
    'COMMENT'
)
```

Esses tokens cobrem:

- **Palavras reservadas:** comandos, tipos e operadores lógicos.
- **Identificadores:** nomes de variáveis e arrays.
- **Literais:** inteiros, reais, strings, caracteres, booleanos.
- **Operadores e símbolos:** aritméticos, relacionais, de atribuição, agrupamento e arrays.
- **Comentários:** `{ ... }`



---

## Parser/Yacc (yaccer.py)

O **parser** utiliza as regras da gramática para construir a árvore sintática e gerar código da VM.

Cada produção da gramática corresponde a uma função Python no arquivo `yaccer.py`, com o prefixo `p_`. Essas funções recebem como argumento a lista `p`, que contém os elementos reconhecidos pela produção. 


---

## Exemplos de Entrada e Saída

### Exemplo 1:

**Entrada (fatorial.pas):**
```pascal
program Fatorial;
var
n, i, fat: integer;
begin
writeln('Introduza um número inteiro positivo:');
readln(n);
fat := 1;
for i := 1 to n do
fat := fat * i;
writeln('Fatorial de ', n, ': ', fat);
end.

```

**Saída:**
```text
START
PUSHS "Introduza um número inteiro positivo:"
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHI 1
STOREG 2
PUSHI 1
STOREG 1
labelstart0:
PUSHG 1
PUSHG 0
INFEQ
JZ labelend1
PUSHG 2
PUSHG 1
MUL
STOREG 2
PUSHG 1
PUSHI 1
ADD
STOREG 1
JUMP labelstart0
labelend1:
PUSHS "Fatorial de "
WRITES
PUSHG 0
WRITEI
PUSHS ": "
WRITES
PUSHG 2
WRITEI
WRITELN
STOP

```


### Exemplo 2: 

**Entrada (isprimo.pas):**
```pascal
program NumeroPrimo;
var
num, i: integer;
primo: boolean;
begin
writeln('Introduza um número inteiro positivo:');
readln(num);
primo := true;
i := 2;
while (i <= (num div 2)) and primo do
begin
if (num mod i) = 0 then
primo := false;
i := i + 1;
end;
if primo then
writeln(num, ' é um número primo')
else
writeln(num, ' não é um número primo')
end.

```

**Saída:**
```text
START
PUSHS "Introduza um número inteiro positivo:"
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHI 1
STOREG 2
PUSHI 2
STOREG 1
labelstart1:
PUSHG 1
PUSHG 0
PUSHI 2
DIV
INFEQ
PUSHG 2
AND
JZ labelend2
PUSHG 0
PUSHG 1
MOD
PUSHI 0
EQUAL
JZ labelend0
PUSHI 0
STOREG 2
labelend0:
PUSHG 1
PUSHI 1
ADD
STOREG 1
JUMP labelstart1
labelend2:
PUSHG 2
JZ labelelse3
PUSHG 0
WRITEI
PUSHS " é um número primo"
WRITES
WRITELN
JUMP labelend4
labelelse3:
PUSHG 0
WRITEI
PUSHS " não é um número primo"
WRITES
WRITELN
labelend4:
STOP

```

### Exemplo 3: 

**Entrada (grades.pas):**
```pascal
program grades;
var
  marks : integer;
  grade : char;
begin
  write('Enter marks: ');
  readln(marks);

  if marks >= 75 then
    grade := 'A'
  else if marks >= 65 then
    grade := 'B'
  else if marks >= 55 then
    grade := 'C'
  else if marks >= 40 then
    grade := 'S'
  else
    grade := 'W';

  writeln('Your grade: ', grade);
end.

```

**Saída:**
```text
START
PUSHS "Enter marks: "
WRITES
WRITELN
READ
ATOI
STOREG 0
PUSHG 0
PUSHI 75
SUPEQ
JZ labelelse6
PUSHS "A"
STOREG 1
JUMP labelend7
labelelse6:
PUSHG 0
PUSHI 65
SUPEQ
JZ labelelse4
PUSHS "B"
STOREG 1
JUMP labelend5
labelelse4:
PUSHG 0
PUSHI 55
SUPEQ
JZ labelelse2
PUSHS "C"
STOREG 1
JUMP labelend3
labelelse2:
PUSHG 0
PUSHI 40
SUPEQ
JZ labelelse0
PUSHS "S"
STOREG 1
JUMP labelend1
labelelse0:
PUSHS "W"
STOREG 1
labelend1:
labelend3:
labelend5:
labelend7:
PUSHS "Your grade: "
WRITES
PUSHG 1
WRITES
WRITELN
STOP
```

### Exemplo 4: Soma de Array

**Entrada (sumlist.pas):**
```pascal
program SomaArray;
var
numeros: array[1..5] of integer;
i, soma: integer;
begin
soma := 0;
writeln('Introduza 5 números inteiros:');
for i := 1 to 5 do
begin
readln(numeros[i]);
soma := soma + numeros[i];
end;
writeln('A soma dos números é: ', soma);
end.
```

**Saída:**
```text
START
PUSHI 0
STOREG 6
PUSHS "Introduza 5 números inteiros:"
WRITES
WRITELN
PUSHI 1
STOREG 5
labelstart0:
PUSHG 5
PUSHI 5
INFEQ
JZ labelend1
PUSHGP
PUSHI 0
PADD
PUSHG 5
PUSHI 1
SUB
READ
ATOI
STOREN
PUSHG 6
PUSHGP
PUSHI 0
PADD
PUSHG 5
PUSHI 1
SUB
LOADN
ADD
STOREG 6
PUSHG 5
PUSHI 1
ADD
STOREG 5
JUMP labelstart0
labelend1:
PUSHS "A soma dos números é: "
WRITES
PUSHG 6
WRITEI
WRITELN
STOP
```


---

## Conclusão

O projeto demonstra como construir um compilador simples para Pascal Standard usando PLY, cobrindo análise léxica, sintática e geração de código intermediário. O sistema suporta variáveis, arrays, controle de fluxo, entrada/saída e expressões, sendo facilmente extensível para mais recursos da linguagem.
