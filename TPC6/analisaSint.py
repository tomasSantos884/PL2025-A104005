from analisaLex import lexer

def analex_input(simb):
    lexer.input(simb)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
    return tokens


"""Reconhece e avalia expressões do tipo Termo { ('+' | '-') Termo }."""
def recExp(tokens):
    node, tokens = recTerm(tokens)
    while tokens and tokens[0][0] in ('PLUS', 'MINUS'):
        op, _ = tokens.pop(0)
        right, tokens = recTerm(tokens)
        node = [op, node, right]
    return node, tokens


"""Reconhece e avalia termos do tipo Factor { ('*' | '/') Factor }."""
def recTerm(tokens):
    node, tokens = recFactor(tokens)
    while tokens and tokens[0][0] in ('TIMES', 'DIV'):
        op, _ = tokens.pop(0)
        right, tokens = recFactor(tokens)
        node = [op, node, right]
    return node, tokens

"""Reconhece e avalia fatores, que podem ser números ou expressões entre parênteses."""
def recFactor(tokens):
    if not tokens:
        raise ValueError("Tokens insuficientes para formar um fator")
    
    token_type, token_value = tokens.pop(0)
    
    if token_type == 'NUM':
        return token_value, tokens
    elif token_type == 'LPAR':
        #Reconhece uma expressão entre parentese
        node, tokens = recExp(tokens)
        if not tokens or tokens[0][0] != 'RPAR':
            raise ValueError("Parêntese direito esperado")
        tokens.pop(0)  #Consome o RPAR
        return node, tokens
    else:
        raise ValueError(f"Token inesperado: {token_type}")


"""Avalia a AST gerada pelo parser."""
def calc(ast):
    if isinstance(ast, int):
        return ast
    if isinstance(ast, list):
        op, esq, dir = ast
        ve = calc(esq)
        vd = calc(dir)
        if op == 'PLUS':
            return ve + vd
        elif op == 'MINUS':
            return ve - vd
        elif op == 'TIMES':
            return ve * vd
        elif op == 'DIV':
            return ve / vd
    raise ValueError("AST inválida")