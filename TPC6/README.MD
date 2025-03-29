# PL2025-A104005 - TPC6

## Título
Parser LL(1) Recursivo Descendente para Expressões Aritméticas

## Data
21 de Março de 2025

## Autor  
- **Nome:** Tomás Araújo Santos 
- **Número:** 104005

## Resumo (`analisaSint.py` e `analisaLex.py`)

- Implementa um parser LL(1) recursivo descendente que reconhece expressões aritméticas e calcula o respetivo valor.
- Define a gramática para expressões aritméticas: Exp -> Term { ('+' | '-') Term } Term -> Factor { ('*' | '/') Factor } Factor -> NUM | '(' Exp ')'

- Componentes principais:
- **Análise Léxica (`analisaLex.py`)**:
  - Transforma a entrada em tokens, como `NUM`, `PLUS`, `MINUS`, `TIMES`, `DIV`, `LPAR`, `RPAR`.
  - Exemplo de entrada: `2 + 3 * 4`
  - Tokens gerados: `[('NUM', 2), ('PLUS', '+'), ('NUM', 3), ('TIMES', '*'), ('NUM', 4)]`
- **Análise Sintática (`analisaSint.py`)**:
  - Implementa as funções `recExp`, `recTerm` e `recFactor` para reconhecer a gramática e construir uma AST (Abstract Syntax Tree).
  - Exemplo de AST gerada para `2 + 3 * 4`:
    ```
    ['PLUS', 2, ['TIMES', 3, 4]]
    ```
- **Avaliação da AST (`calc`)**:
  - Percorre a AST e calcula o valor da expressão.
  - Exemplo: Para a AST `['PLUS', 2, ['TIMES', 3, 4]]`, o resultado é `14`.

- Interação com o utilizador:
- O programa lê uma expressão aritmética, gera os tokens, constrói a AST e calcula o resultado.
- Exemplo de entrada: `67 - (2 + 3 * 4)`
  - Tokens: `[('NUM', 67), ('MINUS', '-'), ('LPAR', '('), ('NUM', 2), ('PLUS', '+'), ('NUM', 3), ('TIMES', '*'), ('NUM', 4), ('RPAR', ')')]`
  - AST: `['MINUS', 67, ['PLUS', 2, ['TIMES', 3, 4]]]`
  - Resultado: `53`

## Lista de Resultados
- [Código-fonte do Lexer](analisaLex.py)
- [Código-fonte do Parser](analisaSint.py)
- [Exemplo de Execução](exec.py)