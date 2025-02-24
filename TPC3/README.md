# PL2025-A104005 - TPC3

## Título
Conversor de MarkDown para HTML

## Data
24 de Fevereiro de 2025

## Autor  
- **Nome:** Tomás Araújo Santos 
- **Número:** 104005
- ![Foto do Autor](../extra/foto.jpeg)

## Resumo (`mdToHTML.py`)

- Lê um ficheiro Markdown e converte-o para HTML
- Suporta os seguintes elementos Markdown:
  - `#` → Converte para `<h1>`
  - `**` → Converte para `<b>`
  - `*` → Converte para `<i>`
  - `[link]` → Converte para `<a href="link">link</a>`
  - `![image]` → Converte para `<img src="image">`
  - `1.` → Converte para lista ordenada `<ol><li>`
- Fecha a lista ordenada (`</ol>`) quando necessário
- Ignora linhas vazias
- Imprime o HTML resultante no terminal

## Lista de Resultados
- [Código-fonte](mdToHTML.py)
- [Ficheiro teste](test.md)