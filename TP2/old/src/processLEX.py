import re
from helper import *
from typing import List


# DEVOLVE UMA STRING COM A DEFINIÇÃO DA FUNÇÃO PARA O FILE LEX
# IMPORTANTE: O FORMATO DA FUNÇÃO TEM DE SER ASSIM!!!
def lex_function(tok: str, regex: str, content: str):

    if content == '':
        res = f"""def t_{tok}(t):
    r'{regex}'
    return t\n\n"""
    else:
        res = f"""def t_{tok}(t):
    r'{regex}'
    {content}
    return t\n\n"""

    return res


# PROCESSA OS TOKENS (CASO ESTEJAM ASSOCIADOS A FUNÇÕES OU NÃO) 
def process_tokens(tok: str, list_regex: List[str]):

    tok_no_func = ""
    tok_func = ""
    tok = re.sub(r' *|\'','',tok)

    for element in list_regex:

        # found an element that is dedicated for token tok
        if re.search(f'\'\w*(?i:{tok})\'',element):

            regex = re.findall(r'^(.*)(?:simpleToken|return)',element)[0]               # apanha toda a regex até à palavra return (exclusive) 
            regex = re.sub(r' +$','',regex)                                             # remove todos os espaços à frente da regex
            regex = re.sub(r'\\{2}',r'\\',regex)

            if re.search('return',element):

                group = (re.findall(r'(?:\(\s*\'(.*?)\'\s*,\s*\'(.*?)\'\s*\))',element))[0]

                tok_func += lex_function(group[0],regex,group[1])

            elif re.search('simpleToken',element):
                tok_no_func += f't_{tok}' + " = r'" + regex + "'\n"

    return tok_func, tok_no_func


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE LEX
def translate_lex(lines_for_LEX: List[str]):

    res = ""
    res_var = ""                                   # a variável literals (que não é obrigatória) não existe no ply-simple
    literals_match = ""
    res_literals = ""
    about_lexer = ""
    run_ignore = False
    run_error = False

    list_regex = [s for s in lines_for_LEX if "return" in s or "simpleToken" in s]

    list_tokens = [s for s in lines_for_LEX if re.search(r'%tokens',s)]                       # string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
    if len(list_tokens) == 0:
        run_tokens = False
    else:
        tokens = (re.findall(r'(?:\[\s?)(.*)(?:\s?\])', list_tokens[0])[0]).split(",")             # list: tokens = ["'VAR'", "'NUMBER'"]
        res_tokens_list = list_tokens[0][list_tokens[0].index("tokens"):] + "\n"
        run_tokens = True

    for line in lines_for_LEX:

        if re.match(r'%ignore',line):
            ignore_match = line
            res_ignore = "t_ignore" + ignore_match[ignore_match.index("ignore") + len("ignore"):] + "\n"
            run_ignore = True                                                       # garante que a variável existe e está introduzida com um %

        elif re.search(r'.*?error',line):
            error_match = line
            error_message = (re.findall(r'(?:f\")(.*)(?:\"\,)',error_match))[0]
            run_error = True                                                        # garante que a variável existe e está introduzida com um %

        elif re.search(r'%literals',line):
            literals_match = line
            res_literals = literals_match[literals_match.index("%")+len("%"):] + "\n" 

        elif re.match(r'%[^tokens]+ *=',line):              # é respeitada a regra "variáveis a começar com %"
            var_match = line
            res_var = var_match[var_match.index("%")+len("%"):] + "\n" 

        if re.match(r'\/%',line):                      # não é uma variável, mas é uma linha importante que deve ser escrita no lex
            about_lexer = line[line.index("/%")+len("/%"):] + "\n"

    if run_tokens and run_error and run_ignore:

        res_toks_func = ""
        res_toks_no_func = ""

        for tok in tokens:
            tok_func, tok_no_func = process_tokens(tok,list_regex)
            res_toks_func = res_toks_func + tok_func
            res_toks_no_func = res_toks_no_func + tok_no_func

        res += res_literals + res_tokens_list + res_var + res_ignore + res_toks_no_func + "\n" + res_toks_func

        res +=  f"""def t_error(t):
    print(f"{error_message}")
    t.lexer.skip(1)\n\n"""
        res += "lexer = lex.lex()\n" + about_lexer

    else:
        raise VariableError

    return res
