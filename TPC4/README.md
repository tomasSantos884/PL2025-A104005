# PL2025-A104005 - TPC4

## Título
Analisador Léxico

## Data
6 de Março de 2025

## Autor  
- **Nome:** Tomás Araújo Santos 
- **Número:** 104005
- ![Foto do Autor](../extra/foto.jpeg)

## Resumo (`lexer.py`)

- Implementa um analisador léxico usando a biblioteca PLY (Python Lex-Yacc).
- Define os seguintes tokens:
  - `SELECT` → Corresponde à palavra-chave `select`
  - `WHERE` → Corresponde à palavra-chave `where`
  - `LIMIT` → Corresponde à palavra-chave `LIMIT`
  - `VAR` → Corresponde a variáveis que começam com `?` seguidas de caracteres alfanuméricos ou sublinhados
  - `STRING` → Corresponde a strings entre aspas duplas
  - `NUMBER` → Corresponde a números inteiros
  - `DOT` → Corresponde ao caractere `.`
  - `BRACE_OPEN` → Corresponde ao caractere `{`
  - `BRACE_CLOSE` → Corresponde ao caractere `}`
  - `IDENTIFIER` → Corresponde a identificadores no formato `prefixo:identificador`
  - `LANGUAGEMARK` → Corresponde a marcações de linguagem que começam com `@` seguidas de letras ou sublinhados
- Ignora espaços, tabs e novas linhas
- Imprime uma mensagem de erro para caracteres ilegais
- Função `tokenize` que lê uma string de entrada e retorna uma lista de tokens

## Lista de Resultados
- [Código-fonte](lexer.py)
