from pickle import FALSE
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

    tok = re.sub(r' *|\'','',tok).upper()

    for element in list_regex:

        # found an element that is dedicated for token tok
        if re.search(f'\'(?i:{tok})\'',element):

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
    res_literals = ""                                   # a variável literals (que não é obrigatória) não existe no ply-simple
    run_literals = True
    run_ignore = False
    run_error = False

    list_regex = [s for s in lines_for_LEX if "return" in s or "simpleToken" in s]

    list_tokens = [s for s in lines_for_LEX if re.search(r'% ?tokens',s)]                       # string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
    if len(list_tokens) == 0:
        run_tokens = False
    else:
        tokens = (re.findall(r'(?:\[\s?)(.*)(?:\s?\])', list_tokens[0])[0]).split(",")             # list: tokens = ["'VAR'", "'NUMBER'"]
        res_tokens_list = list_tokens[0][list_tokens[0].index("tokens"):] + "\n"
        run_tokens = True

    for line in lines_for_LEX:

        if re.match(r'% *literals',line):              # é respeitada a regra "variáveis a começar com %"
            literals_match = line
            res_literals = literals_match[literals_match.index("literals"):] + "\n" 

        elif re.match(r'literals',line):               # existe variável literals, mas não começa com %
            run_literals = False

        elif re.match(r'% *ignore',line):
            ignore_match = line
            res_ignore = "t_ignore" + ignore_match[ignore_match.index("ignore") + len("ignore"):] + "\n"
            run_ignore = True

        elif re.search(r'.*?error',line):
            error_match = line
            error_message = (re.findall(r'(?:f\")(.*)(?:\"\,)',error_match))[0]
            run_error = True

    if run_tokens & run_literals & run_error & run_ignore:

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

    else:
        raise NameError

    return res
