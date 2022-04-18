import re
from typing import List


# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def get_lex_yacc(lines: List[str]):

    pos = 0
    lines_for_LEX = []                      # guarda todo o conteúdo para o file lex
    lines_for_YACC = []                     # guarda todo o conteúdo para o file yacc

    for line in lines:
        if re.search(r'LEX',line):
            pos_lex = pos                   # pos em que começa o conteúdo para o file lex
        if re.search(r'YACC',line):
            pos_yacc = pos                  # pos em que começa o conteúdo para o file yacc
        pos = pos + 1

    for line in lines[pos_lex+1:pos_yacc]:
        if not re.search(r'^$',line) and not re.match(r'^%+$',line):          # remove empty lines or lines like %%
            lines_for_LEX.append(line)
    
    for line in lines[pos_yacc+1:]:
        if not re.search(r'^$',line) and not re.match(r'^%+$',line):          # remove empty lines or lines like %%
            lines_for_YACC.append(line)
    
    return lines_for_LEX, lines_for_YACC


# DEVOLVE UMA STRING COM A DEFINIÇÃO DA FUNÇÃO PARA O FILE LEX
# IMPORTANTE: O FORMATO DA FUNÇÃO TEM DE SER ASSIM!!!
def lex_function(tok: str, regex: str, t, type: str):

    if type == "float":
        res = f"""def t_{tok}(t):
    r'{regex}'
    t.value = float(t.value)
    return t\n\n"""
    elif type == "int":
        res = f"""def t_{tok}(t):
    r'{regex}'
    t.value = int(t.value)
    return t\n\n"""
    elif type == "str":
        res = f"""def t_{tok}(t):
    r'{regex}'
    return t\n\n"""
    return res


# PROCESSA OS TOKENS (CASO ESTEJAM ASSOCIADOS A FUNÇÕES OU NÃO) 
def process_tokens(tok: str, list_returns: List[str], list_no_returns: List[str]):

    tok = re.sub(r' *',r'',tok)

    aux = [s for s in list_returns if tok in s]

    # in case the token has a function associated
    if len(aux) != 0:
        regex = re.findall(r'^(.*)(?:return)',aux[0])[0]
        regex = re.sub(r' +$','',regex)
        regex = re.sub(r'\\{2}',r'\\',regex)

        if re.match(f'{regex}',"1.0"):
            type = "float"
        elif re.match(f'{regex}',"1"):
            type = "int"
        else:
            type = "str"

        tok = re.sub(r'\'',r'',tok)
        tok_func = lex_function(tok,regex,"t",type)
        tok_no_func = ""

    # in case the token DOESN'T have a function associated
    else:
        tok = (re.sub(r'\'',r'',tok)).lower()
        tok_match = [s for s in list_no_returns if tok in s][0]
        content = tok_match[tok_match.index(f'{tok}') + len(f'{tok}'):]

        tok_func = ""
        tok_no_func = f't_{tok}' + content + "\n"

    return tok_func, tok_no_func

# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def translate_lex(lines_for_LEX: List[str]):

    res = ""

    list_returns = [s for s in lines_for_LEX if "return" in s]
    list_no_returns = [s for s in lines_for_LEX if s not in list_returns]

    tokens_match = [s for s in list_no_returns if "tokens" in s][0]                     # string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
    list_no_returns.remove(tokens_match)
    tokens = (re.findall(r'(?:\[\s?)(.*)(?:\s?\])', tokens_match)[0]).split(",")      # list: tokens = ["'VAR'", "'NUMBER'"]
    res_tokens_list = tokens_match[1:] + "\n"

    for line in lines_for_LEX:

        if re.search(r'literals',line):     # LITERALS
            literals_match = line
            res_literals = literals_match[1:] + "\n"
            list_no_returns.remove(literals_match)

        elif re.search(r'ignore',line):       # IGNORE
            ignore_match = line
            res_ignore = "t_ignore" + ignore_match[ignore_match.index("ignore") + len("ignore"):] + "\n"
            list_no_returns.remove(line)

        elif re.search(r'error',line):
            error_match = line
            error_message = (re.findall(r'(?:f\")(.*)(?:\"\,)',error_match))[0]
            list_no_returns.remove(line)

    res_toks_func = ""
    res_toks_no_func = ""

    for tok in tokens:
        tok_func, tok_no_func = process_tokens(tok,list_returns,list_no_returns)
        res_toks_func = res_toks_func + tok_func
        res_toks_no_func = res_toks_no_func + tok_no_func

    res = res + res_tokens_list + res_literals + res_ignore + res_toks_no_func + "\n" + res_toks_func

    res = res + f"""def t_error(t):
    print(f"{error_message}")
    t.lexer.skip(1)\n\n"""
    res = res + "lexer = lex.lex()"

    return res


# ABRE UM FICHEIRO E DEVOLVE UMA LISTA COM O SEU CONTEÚDO
def open_file():
    input_name = input("[CSV] Insert file name (extension included): ")

    try:	
        file = open("../input/"+input_name)
    except OSError:
        print(f"[ERROR] Can't locate CSV file \"{input_name}\".\n")
        input("[PRESS ENTER TO CONTINUE]")
        return -1

    if file:
        lines = file.read().splitlines()
        print("[FILE] Opened successfully.")
        input("[PRESS ENTER TO CONTINUE]")
        file.close()
        return input_name, lines


# CRIA E ESCREVE NO FILE LEX
def write_file_lex(input_name:str, res0: str):

    imports = "import ply.lex as lex"
    res = imports + "\n\n" + res0

    input_name = re.sub(r'\.(.*)',r'',input_name)
    outputFile = open("../output/"+f'{input_name}_lex.py','w')
    outputFile.write(res)
    outputFile.close

    print("[FILE] Translated LEX successfully.")
    input("[PRESS ENTER TO CONTINUE]")