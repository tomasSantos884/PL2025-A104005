from analisaSint import analex_input, recExp, calc


def main():
    exp = input("Input: ")
    try:
        tokens = analex_input(exp)
        print("Tokens:", tokens)
        ast, resto = recExp(tokens)
        if resto:
            print("Erro: tokens não consumidos:", resto)
        else:
            print("AST Gerada:", ast)
            print("Resultado:", calc(ast))
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()