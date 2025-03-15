import json
import time
import re

class Product:
    def __init__(self, cod, nome, quant, preco):
        self.cod = cod
        self.nome = nome
        self.quant = quant
        self.preco = preco

def get_stock():
    with open('stock.json', 'r') as f:
        stock_data = json.load(f)["stock"]
    stock = [Product(**item) for item in stock_data]
    return stock

def save_stock(stock):
    with open('stock.json', 'w') as f:
        stock_data = [item.__dict__ for item in stock]
        json.dump({"stock": stock_data}, f)

def tokenize(txt):
    tokens = re.findall(r'\b\w+\b', txt)
    return tokens

def parse_money(money_str):
    total = 0
    coins = re.findall(r'(\d+)([ce])', money_str)
    for amount, unit in coins:
        if unit == 'e':
            total += int(amount) * 100
        elif unit == 'c':
            total += int(amount)
    return total

def init_machine():
    stock = get_stock()
    date = time.localtime()
    saldo = 0
    
    print(f'{date.tm_year}-{date.tm_mon}-{date.tm_mday}, Stock carregado, Estado atualizado.')
    print('Bom dia. Estou disponível para atender o seu pedido.')
    
    opt = input('>> ')
    
    while(opt.upper() != 'SAIR'):
        tokens = tokenize(opt)
        
        if tokens[0].upper() == 'LISTAR':
            print('cod |     nome     | quantidade | preço')
            print('-----------------------------------------------')
            
            for product in stock:
                print(f'{product.cod} | {product.nome}    | {product.quant} | {product.preco}')
        
        elif tokens[0].upper() == 'MOEDA':
            money_str = ' '.join(tokens[1:])
            saldo += parse_money(money_str)
            print(f'Saldo = {saldo // 100}e{saldo % 100}c')
        
        elif tokens[0].upper() == 'SELECIONAR':
            cod = tokens[1]
            found = False
            for product in stock:
                if product.cod == cod:
                    found = True
                    if product.quant > 0:
                        if saldo >= product.preco * 100:
                        
                            product.quant -= 1
                            saldo -= int(product.preco * 100)
                            print(f'Pode retirar o produto dispensado "{product.nome}"')
                            print(f'Saldo = {saldo // 100}e{saldo % 100}c')
                        else:
                            print(f'Saldo insuficiente para satisfazer o seu pedido')
                            print(f'Saldo = {saldo}c; Pedido = {int(product.preco * 100)}c')
                    else:
                            print('Produto fora de stock.')    
                    
                    break
            if not found:
                print('Produto não encontrado.')
        
        opt = input('>> ')
    
    troco = saldo
    moedas = []
    for value, name in [(50, '50c'), (20, '20c'), (10, '10c'), (5, '5c'), (2, '2c'), (1, '1c')]:
        while troco >= value:
            troco -= value
            moedas.append(name)
    print(f'Pode retirar o troco: {", ".join(moedas)}.')
    print('Até à próxima')
    
    save_stock(stock)

init_machine()