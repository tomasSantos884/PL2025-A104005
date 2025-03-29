""" 

2+3
67-(2+3*4)
(9-2)*(13-4) 

"""

import ply.lex as lex
import re


tokens = (
    'NUM', 
    'LPAR', 
    'RPAR', 
    'PLUS',
    'MINUS',  
    'TIMES', 
    'DIV'  
)

t_LPAR = r'\('
t_RPAR = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/'
t_ignore = ' \t'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print(f'Carácter desconhecido: {t.value[0]} na linha {t.lexer.lineno}')
    t.lexer.skip(1)
    
    
lexer = lex.lex()