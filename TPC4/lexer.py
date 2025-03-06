import ply.lex as lex

# Lista de tokens
tokens = (
    'SELECT', 'WHERE', 'LIMIT',
    'VAR', 'STRING', 'NUMBER',
    'DOT', 'BRACE_OPEN', 'BRACE_CLOSE', 'IDENTIFIER', 'LANGUAGEMARK'
)

# Expressões regulares para tokens simples
t_SELECT = r'select'
t_WHERE = r'where'
t_LIMIT = r'LIMIT'
t_DOT = r'\.'
t_BRACE_OPEN = r'\{'
t_BRACE_CLOSE = r'\}'



def t_VAR(t):
    r'\?[a-zA-Z_]\w*'
    return t

def t_LANGUAGEMARK(t):
    r'@[a-zA-Z_]+'
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z]\w*:[a-zA-Z]\w*|[a-zA-Z]{1}\s'
    return t


t_ignore = ' \t\n'


def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)


def tokenize(txt):
    lexer = lex.lex()
    lexer.input(txt)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(f"LexToken({tok.type},{tok.value},{tok.lineno},{tok.lexpos})")
    return tokens_list

# Exemplo de uso
msg = """
select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
"""

tokens_output = tokenize(msg)
for token in tokens_output:
    print(token)