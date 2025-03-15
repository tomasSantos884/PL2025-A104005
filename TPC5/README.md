# PL2025-A104005 - TPC5

## Título
Máquina de Vendas Automática

## Data
15 de Março de 2025

## Autor  
- **Nome:** Tomás Araújo Santos 
- **Número:** 104005
- ![Foto do Autor](../extra/foto.jpeg)

## Resumo (`vendingM.py`)

- Implementa uma máquina de vendas automática que permite listar produtos, inserir moedas e selecionar produtos.
- Define a classe `Product` com os seguintes atributos:
  - `cod` → Código do produto
  - `nome` → Nome do produto
  - `quant` → Quantidade disponível
  - `preco` → Preço do produto
- Funções principais:
  - `get_stock` → Lê o stock de um arquivo JSON e retorna uma lista de objetos `Product`
  - `save_stock` → Guarda o stock atualizado de volta no arquivo JSON
  - `tokenize` → Tokeniza a entrada do utilizador usando expressões regulares
  - `parse_money` → Converte uma string de moedas num valor total em cêntimos
  - `init_machine` → Inicializa a máquina de vendas e gere a interação com o utilizador
- Interação com o utilizador:
  - `LISTAR` → Lista todos os produtos disponíveis
  - `MOEDA` → Insere moedas e atualiza o saldo
  - `SELECIONAR` → Seleciona um produto para compra
  - `SAIR` → Finaliza a interação e retorna o troco

## Lista de Resultados
- [Código-fonte](vendingM.py)
- [Stock](stock.json)