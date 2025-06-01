import ply.lex as lex



# Lista de nomes de tokens
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

# Regras de expressões regulares para tokens simples
t_ASSIGNMENT = r':='
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVISION = r'/'
t_EQ = r'='
t_NEQ = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_DOTDOT = r'\.\.'

# Palavras reservadas
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'begin': 'BEGIN',
    'end': 'END',
    
    'write': 'WRITE',
    'writeln': 'WRITELN',
    'readln': 'READLN',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'to': 'TO',
    'downto': 'DOWNTO',
    
    'integer': 'TINTEGER',
    'real': 'TREAL',
    'string': 'TSTRING',
    'char': 'TCHAR',
    'boolean': 'TBOOLEAN',
    'true': 'BOOLEAN',
    'false': 'BOOLEAN',
    
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'div': 'DIV',
    'mod': 'MOD',
    
    'array': 'ARRAY',
    'of': 'OF',
}

# Literais numéricos
def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regras para o token BOOLEAN
def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False  # Converte para valores booleanos
    return t

# Identificadores e palavras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.value = t.value.lower()  # Converte para minúsculas
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verifica se é uma palavra reservada
    return t

# Literais de caractere
def t_CHAR(t):
    r'\'[a-zA-Z]\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Literais de string
def t_STRING(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t


def t_COMMENT(t):
	r"{[^}]*}"

# Define uma regra para rastrear números de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados (espaços e tabulações)
t_ignore = ' \t'

# Regra de tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()
