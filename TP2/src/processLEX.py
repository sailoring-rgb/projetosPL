import re
from typing import List


# DEVOLVE UMA STRING COM A DEFINIÇÃO DA FUNÇÃO PARA O FILE LEX
# IMPORTANTE: O FORMATO DA FUNÇÃO TEM DE SER ASSIM!!!
def lex_function(tok: str, regex: str, type: str):

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
def process_tokens(tok: str, list_regex: List[str]):

    tok = re.sub(r' *|\'','',tok)

    for element in list_regex:

        # found an element that is dedicated for token tok
        if re.search(f'{tok}',element):

            regex = re.findall(r'^(.*)(?:simpleToken|return)',element)[0]               # apanha toda a regex até à palavra return (exclusive) 
            regex = re.sub(r' +$','',regex)                                             # remove todos os espaços à frente da regex
            regex = re.sub(r'\\{2}',r'\\',regex)

            if re.search('return',element):

                if re.match(f'{regex}',"1.0"):                                          # se a regex apanhar floats, então o tipo é um float
                    type = "float" 
                elif re.match(f'{regex}',"1"):                                          # se a regex apanhar ints, então o tipo é um int
                    type = "int"
                else:
                    type = "str"                                                        # caso contrário, o tipo é tratado como uma string

                tok_func = lex_function(tok,regex,type)
                tok_no_func = ""

            elif re.search('simpleToken',element):
                
                tok_func = ""
                tok_no_func = f't_{tok}' + " = r'" + regex + "'\n"

    return tok_func, tok_no_func


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE LEX
def translate_lex(lines_for_LEX: List[str]):

    res = ""

    list_regex = [s for s in lines_for_LEX if "return" in s or "simpleToken" in s]

    list_tokens = [s for s in lines_for_LEX if "tokens" in s][0]                        # string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
    tokens = (re.findall(r'(?:\[\s?)(.*)(?:\s?\])', list_tokens)[0]).split(",")         # list: tokens = ["'VAR'", "'NUMBER'"]
    res_tokens_list = list_tokens[1:] + "\n"

    for line in lines_for_LEX:

        if re.search(r'literals',line):                                                  # LITERALS
            literals_match = line
            res_literals = literals_match[1:] + "\n"

        elif re.search(r'ignore',line):                                                  # IGNORE
            ignore_match = line
            res_ignore = "t_ignore" + ignore_match[ignore_match.index("ignore") + len("ignore"):] + "\n"

        elif re.search(r'error',line):
            error_match = line
            error_message = (re.findall(r'(?:f\")(.*)(?:\"\,)',error_match))[0]

    res_toks_func = ""
    res_toks_no_func = ""

    for tok in tokens:
        tok_func, tok_no_func = process_tokens(tok,list_regex)
        res_toks_func = res_toks_func + tok_func
        res_toks_no_func = res_toks_no_func + tok_no_func

    res += res_tokens_list + res_literals + res_ignore + res_toks_no_func + "\n" + res_toks_func

    res +=  f"""def t_error(t):
    print(f"{error_message}")
    t.lexer.skip(1)\n\n"""
    res += "lexer = lex.lex()"

    return res
