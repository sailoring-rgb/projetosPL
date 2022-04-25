import re
from typing import List


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

    tokens_match = [s for s in list_no_returns if "tokens" in s][0]                   # string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
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

    res += res_tokens_list + res_literals + res_ignore + res_toks_no_func + "\n" + res_toks_func

    res +=  f"""def t_error(t):
    print(f"{error_message}")
    t.lexer.skip(1)\n\n"""
    res += "lexer = lex.lex()"

    return res
