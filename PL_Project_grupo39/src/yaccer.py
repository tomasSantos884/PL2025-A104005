import ply.yacc as yacc
from lexer import tokens 
import sys

symbol_table = {}
symbol_counter = 0
mem_counter = 0 

label_counter = 0
def new_label(prefix):
    global label_counter
    label = f"{prefix}{label_counter}"
    label_counter += 1
    return label

symbol_types = {}

def p_program(p):
    'Program : Header SEMICOLON Block DOT'
    p[0] = f"START{p[3]}STOP"

def p_header(p):
    'Header : PROGRAM IDENTIFIER'
    p[0] = "" 

def p_block(p):
    'Block : Var_declaration_block Code_block'
    p[0] = f"{p[1]}\n{p[2]}"

def p_var_declaration_block(p):
    '''Var_declaration_block : VAR Var_list
                             | '''
    if len(p) == 3:
        p[0] = p[2] 
    else:
        p[0] = ""

def p_var_list(p):
    '''Var_list : Var_declaration Var_list
                | Var_declaration'''
    if len(p) == 3:
        p[0] = f"{p[1]}\n{p[2]}"
    else:
        p[0] = p[1]

def p_var_declaration(p):
    'Var_declaration : Identifier_list COLON Type SEMICOLON'
    global mem_counter
    id_list = [v.strip() for v in p[1].split(',')]
    tipo = p[3]
    if isinstance(tipo, tuple) and tipo[0] == 'array':
        start, end, base_type = tipo[1], tipo[2], tipo[3]
        size = end - start + 1
        for var in id_list:
            symbol_table[var] = {
                'type': 'array',
                'start': start,
                'end': end,
                'base': base_type,
                'mem_start': mem_counter
            }
            symbol_types[var] = base_type 
            mem_counter += size
    else:
        for var in id_list:
            symbol_table[var] = mem_counter
            symbol_types[var] = tipo      
            mem_counter += 1
    p[0] = ""

def p_identifier_list(p):
    '''Identifier_list : IDENTIFIER COMMA Identifier_list
                       | IDENTIFIER'''
    global symbol_counter
    if len(p) == 4:
        # Adiciona o identificador atual à tabela, se não existir
        if p[1] not in symbol_table:
            symbol_table[p[1]] = symbol_counter
            symbol_counter += 1
        # Junta os identificadores em uma string separada por vírgula
        p[0] = f"{p[1]}, {p[3]}"
    else:
        if p[1] not in symbol_table:
            symbol_table[p[1]] = symbol_counter
            symbol_counter += 1
        p[0] = p[1]

def p_type(p):
    '''Type : TINTEGER
            | TREAL
            | TSTRING
            | TCHAR
            | TBOOLEAN
            | Array_type'''
    p[0] = p[1]

def p_array_type(p):
    'Array_type : ARRAY LBRACKET integer DOTDOT integer RBRACKET OF Type'
    p[0] = ('array', p[3], p[5], p[8])

def p_code_block(p):
    'Code_block : BEGIN Statements END'
    p[0] = f"{p[2]}"

def p_statements(p):
    '''Statements : Statement SEMICOLON Statements
                  | Statement'''
    if len(p) == 4:
        p[0] = f"{p[1]}\n{p[3]}"
    else:
        p[0] = p[1]

def p_statement(p):
    '''Statement : Assignment_statement
                 | Code_block
                 | If_statement
                 | While_statement
                 | For_statement
                 | Write_statement
                 | Readln_statement
                 | '''
    if len(p) == 1:
        p[0] = ""  
    else:
        if isinstance(p[1], tuple):
            p[0] = p[1][0]
        else:
            p[0] = p[1]

def p_if_statement(p):
    '''If_statement : IF Expression THEN Statement ELSE Statement
                    | IF Expression THEN Statement'''
    if len(p) == 7:
        label_else = new_label("labelelse")
        label_end = new_label("labelend")
        p[0] = f"{p[2]}\nJZ {label_else}\n{p[4]}\nJUMP {label_end}\n{label_else}:\n{p[6]}\n{label_end}:"
    else:
        label_end = new_label("labelend")
        p[0] = f"{p[2]}\nJZ {label_end}\n{p[4]}\n{label_end}:"

def p_while_statement(p):
    'While_statement : WHILE Expression DO Statement'
    label_start = new_label("labelstart")
    label_end = new_label("labelend")
    p[0] = f"{label_start}:\n{p[2]}\nJZ {label_end}\n{p[4]}\nJUMP {label_start}\n{label_end}:"

def p_for_statement(p):
    '''For_statement : FOR Assignment_statement TO Expression DO Statement
                     | FOR Assignment_statement DOWNTO Expression DO Statement'''
    label_start = new_label("labelstart")
    label_end = new_label("labelend")
    assign_code, var_name = p[2]  
    var_idx = symbol_table[var_name]
    if p[3].upper() == "TO":
        cmp_op = "INFEQ"
        inc = f"PUSHG {var_idx}\nPUSHI 1\nADD\nSTOREG {var_idx}"
    else:
        cmp_op = "SUPEQ"
        inc = f"PUSHG {var_idx}\nPUSHI 1\nSUB\nSTOREG {var_idx}"
    p[0] = (
        f"{assign_code}\n"
        f"{label_start}:\n"
        f"PUSHG {var_idx}\n{p[4]}\n{cmp_op}\nJZ {label_end}\n"
        f"{p[6]}\n"
        f"{inc}\n"
        f"JUMP {label_start}\n"
        f"{label_end}:"
    )

def p_write_statement(p):
    '''Write_statement : WRITE LPAREN Param_list RPAREN
                       | WRITELN LPAREN Param_list RPAREN'''
    write_code = []
    for code, tipo in p[3]:
        if tipo == "string" or tipo == "char":
            write_code.append(f"{code}\nWRITES")
        elif tipo == "int":
            write_code.append(f"{code}\nWRITEI")
        elif tipo == "real":
            write_code.append(f"{code}\nWRITEF")
        else:
            write_code.append(f"{code}\nWRITES")  # fallback
    if p[1] == "WRITE":
        p[0] = "\n".join(write_code)
    else:
        p[0] = "\n".join(write_code) + "\nWRITELN"

def p_param_list(p):
    '''Param_list : Param_list COMMA Param
                  | Param'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_param(p):
    '''Param : Expression'''
    import re
    if isinstance(p[1], tuple):
        p[0] = p[1]
    elif isinstance(p[1], int):
        p[0] = (f"PUSHI {p[1]}", "int")
    elif isinstance(p[1], float):
        p[0] = (f"PUSHF {p[1]}", "real")
    elif isinstance(p[1], str) and p[1].startswith('PUSHG'):
        # Extrai o índice e procura o nome da variável
        match = re.match(r'PUSHG (\d+)', p[1])
        if match:
            idx = int(match.group(1))
            for var, val in symbol_table.items():
                if isinstance(val, int) and val == idx:
                    tipo = symbol_types.get(var, "int")
                    if tipo == "TCHAR":
                        p[0] = (p[1], "char")
                    elif tipo == "TSTRING":
                        p[0] = (p[1], "string")
                    elif tipo == "TREAL":
                        p[0] = (p[1], "real")
                    else:
                        p[0] = (p[1], "int")
                    break
            else:
                p[0] = (p[1], "int")
        else:
            p[0] = (p[1], "int")
    elif isinstance(p[1], str) and p[1].startswith('PUSHS'):
        p[0] = (p[1], "string")
    else:
        p[0] = (p[1], "unknown")

def p_readln_statement(p):
    '''Readln_statement : READLN LPAREN IDENTIFIER RPAREN
                        | READLN LPAREN IDENTIFIER LBRACKET Expression RBRACKET RPAREN'''
    if len(p) == 5:
        p[0] = f"READ\nATOI\nSTOREG {symbol_table[p[3]]}"
    else:
        arr = symbol_table[p[3]]
        base_idx = arr['mem_start']
        start = arr['start']
        code = (
            f"PUSHGP\n"
            f"PUSHI {base_idx}\n"
            f"PADD\n"
            f"{p[5]}\n"          
            f"PUSHI {start}\n"
            f"SUB\n"
            f"READ\n"
            f"ATOI\n"
            f"STOREN"
        )
        p[0] = code

def p_assignment_statement(p):
    '''Assignment_statement : IDENTIFIER ASSIGNMENT Expression
                           | IDENTIFIER LBRACKET Expression RBRACKET ASSIGNMENT Expression'''
    if len(p) == 4:
        p[0] = (f"{p[3]}\nSTOREG {symbol_table[p[1]]}", p[1])
    else:
        arr = symbol_table[p[1]]
        base_idx = arr['mem_start']
        start = arr['start']
        code = (
            f"PUSHGP\n"
            f"PUSHI {base_idx}\n"
            f"PADD\n"
            f"{p[3]}\n"           
            f"{p[6]}\n"          
            f"PUSHI {start}\n"
            f"SUB\n"
            f"STOREN"
        )
        p[0] = (code, p[1])
        


def p_expression(p):
    '''Expression : Expression And_or Expression_m
                  | Expression_m'''
    if len(p) == 4:
        op = "AND" if p[2].upper() == "AND" else "OR"
        p[0] = f"{p[1]}\n{p[3]}\n{op}"
    else:
        p[0] = p[1]

def p_expression_m(p):
    '''Expression_m : Expression_s
                    | Expression_m Sign Expression_s'''
    if len(p) == 4:
        op_map = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL',
            '/': 'DIVF',
            'DIV': 'DIV',
            'MOD': 'MOD',
            '=': 'EQUAL',
            '<': 'INF',
            '<=': 'INFEQ',
            '>': 'SUP',
            '>=': 'SUPEQ',
            '<>': 'NEQ'
        }
        key = p[2].upper() if isinstance(p[2], str) else p[2]
        p[0] = f"{p[1]}\n{p[3]}\n{op_map[key]}"
    else:
        p[0] = p[1]

def p_expression_s(p):
    '''Expression_s : Element
                    | Expression_s Psign Element'''
    if len(p) == 4:
        op_map = {'*': 'MUL', '/': 'DIVF'}
        key = p[2].upper() if isinstance(p[2], str) else p[2]
        p[0] = f"{p[1]}\n{p[3]}\n{op_map[key]}"
    else:
        p[0] = p[1]

def p_and_or(p):
    '''And_or : AND
              | OR'''
    p[0] = p[1]

def p_psign(p):
    '''Psign : TIMES
             | DIVISION'''
    p[0] = p[1]

def p_sign(p):
    '''Sign : PLUS
            | MINUS
            | DIV
            | MOD
            | EQ
            | NEQ
            | LT
            | LTE
            | GT
            | GTE'''
    p[0] = p[1]

def p_element(p):
    '''Element : IDENTIFIER
               | IDENTIFIER LBRACKET Expression RBRACKET
               | real
               | integer
               | string
               | char
               | boolean
               | LPAREN Expression RPAREN
               | NOT Element'''
    if len(p) == 5:
        arr = symbol_table[p[1]]
        base_idx = arr['mem_start']
        start = arr['start']
        p[0] = (
            f"PUSHGP\n"
            f"PUSHI {base_idx}\n"
            f"PADD\n"
            f"{p[3]}\n"
            f"PUSHI {start}\n"
            f"SUB\n"
            f"LOADN"
        )
    elif len(p) == 4:
        p[0] = f"{p[2]}"
    elif len(p) == 3:
        p[0] = f"{p[2]}\nNOT"
    elif isinstance(p[1], bool):
        p[0] = f"PUSHI {int(p[1])}"
    elif isinstance(p[1], str) and p.slice[1].type == "IDENTIFIER":
        p[0] = f"PUSHG {symbol_table[p[1]]}"
    elif isinstance(p[1], str) and not p[1].isdigit():
        p[0] = f'PUSHS "{p[1]}"'
    else:
        p[0] = f"PUSHI {p[1]}"
        
        

def p_real(p):
    'real : REAL'
    p[0] = p[1]

def p_integer(p):
    'integer : INTEGER'
    p[0] = p[1]

def p_string(p):
    'string : STRING'
    p[0] = p[1]

def p_char(p):
    'char : CHAR'
    p[0] = p[1]

def p_boolean(p):
    'boolean : BOOLEAN'
    p[0] = int(p[1])  # Converte True/False para 1/0

def p_error(p):
    print("Syntax error!", p)

parser = yacc.yacc()

if __name__ == "__main__":

    source = sys.argv[1]
    with open(source, 'r') as file:
        txt = file.read()

    
    result = parser.parse(txt)

    
    if result:
        print(result)
    else:
        print("Erro: O parser não gerou nenhum resultado.")