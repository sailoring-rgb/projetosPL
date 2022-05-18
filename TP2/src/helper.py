import re
from typing import List
from xxlimited import new

###################################################### EXCEPTIONS ######################################################
class GrammarError(Exception):
    """Raised when no grammar is defined"""
    pass

class VariableError(Exception):
    """Raised when variables are missing or not correctly introduced"""
    pass
#######################################################################################################################

# ABRE UM FICHEIRO E DEVOLVE UMA LISTA COM O SEU CONTEÚDO
def open_file(input_name:str, mode:str):
    file = open("../input/"+input_name)
    
    if not file:
        raise FileNotFoundError
    if mode == 'LEX':
        lines = file.read().splitlines()
    elif mode == 'YACC':
        lines = file.read()
    else:
        lines = ''
    file.close()
    print("\033[96m[" + input_name[:-4] + "]\033[0m\033[92m opened successfully.\033[0m")
    return lines

# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def get_lex_yacc(lines: List[str]):

    pos = 0
    pos_lex = -1
    pos_yacc = -1
    lex_exists = False
    yacc_exists = False
    lines_for_LEX = []                      # guarda todo o conteúdo para o file lex
    lines_for_YACC = []                     # guarda todo o conteúdo para o file yacc

    for line in lines:
        if re.search(r'%% *LEX *%%',line):
            pos_lex = pos                   # pos em que começa o conteúdo para o file lex
            lex_exists = True
        if re.search(r'%% *YACC *%%',line):
            pos_yacc = pos                  # pos em que começa o conteúdo para o file yacc
            yacc_exists = True
        pos = pos + 1

    if pos_lex > pos_yacc and yacc_exists and lex_exists:
        # for yacc
        for line in lines[pos_yacc+1:pos_lex]:
            if not re.search(r'^$',line):          # remove empty lines or lines like %%
                lines_for_YACC.append(line)
        # for lex
        for line in lines[pos_lex+1:]:
            if not re.search(r'^$',line):          # remove empty lines or lines like %%
                lines_for_LEX.append(line)

    elif lex_exists and yacc_exists:
        # for lex
        for line in lines[pos_lex+1:pos_yacc]:
            if not re.search(r'^$',line):          # remove empty lines or lines like %%
                lines_for_LEX.append(line)
        # for yacc
        for line in lines[pos_yacc+1:]:
            if not re.search(r'^$',line):          # remove empty lines or lines like %%
                lines_for_YACC.append(line)

    elif lex_exists and not yacc_exists:
        # for lex
        for line in lines[pos_lex+1:]:
            if not re.search(r'^$',line):          # remove empty lines or lines like %%
                lines_for_LEX.append(line)

    elif not lex_exists and yacc_exists:
        # for yacc
        for line in lines[pos_yacc+1:]:
            if not re.search(r'^$',line):          # remove empty lines or lines like %%
                lines_for_YACC.append(line)
                
    return lex_exists, yacc_exists, lines_for_LEX, lines_for_YACC


########################################################################################################################################

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

            regex = re.findall(r'^%\) *(.*)(?:simpleToken|return)',element)[0]               # apanha toda a regex até à palavra return (exclusive) 
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

    list_regex = [s for s in lines_for_LEX if "return" in s or "simpleToken" in s]

    list_tokens = [s for s in lines_for_LEX if re.search(r'%tokens',s)]                       # string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
    tokens = (re.findall(r'(?:\[\s?)(.*)(?:\s?\])', list_tokens[0])[0]).split(",")             # list: tokens = ["'VAR'", "'NUMBER'"]
    res_tokens_list = list_tokens[0][list_tokens[0].index("tokens"):] + "\n"

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

    return res

# CRIA E ESCREVE NO FILE LEX
def write_file_lex(input_name:str, res0: str):

    imports = "import ply.lex as lex"
    res = imports + "\n\n" + res0

    input_name = re.sub(r'\.(.*)',r'',input_name)
    outputFile = open("../output/"+f'{input_name}_lex.py','w')
    outputFile.write(res)
    outputFile.close

    print("\033[96m[" + input_name + "]\033[92m translated LEX successfully.\033[0m")

########################################################################################################################################

# PROCESSA A GRAMÁTICA RECEBIDA E DEVOLVE UMA STRING COM TODAS AS FUNÇÕES PARA O FILE YACC
def process_grammar(grammar: List[str]):
    i = 1
    res_grammar = ""
    defGrammar = ["# GRAMMAR:"]

    for line in grammar:
        if line != "":
            # exemplo =                         stat : VAR '=' exp              { ts[t[1]] = t[3] }
            # primeiro termo do grupo =         stat
            # segundo termo do grupo =          VAR '=' exp
            # terceiro termo do grupo =         ts[t[1]] = t[3]
            group = (re.findall(r'([^: ]+)(?: *: *(.*?) {2,})(?:{ *(.*?) *})',line))[0]

            # process a production of grammar
            prod = re.sub(r'( %.*)','',group[1])     # remover, por exemplo, %prec UMINUS

            # exemplo =         ts[t[1]] = t[3]
            # op =              [('ts[', 't', '[1]'), ('] = ', 't', '[3]')]
            # isto serve para substituir o segundo termo de um tuplo (neste caso, t) por um p
            op = re.findall(r'(.*?[^A-Za-z]?)([A-Za-z])(\[\d+\]+\)?)',group[2])

            calc = ""
            for s in op:
                s = (s[0],'p',s[2])
                calc += "".join(s)

            # build grammar as comments
            if any(f'{group[0]} ->' in s for s in defGrammar):
                defGrammar.append(f"# p{i}:      | {prod}")
            else: defGrammar.append(f"# p{i}:    {group[0]} -> {prod}")

            res_grammar += f"""def p_{group[0]}_p{i}(p):
    "{group[0]} : {prod}"
    {calc}\n\n"""
            i = i+1
    
    return defGrammar, res_grammar


# PROCESSA UMA FUNÇÃO DESTINADA AO FILE YACC
def process_function(line: str, i: int, res_error: str, res_functions: str):

    def_match = ""
    newFunctions = []

    if re.search(r'^\~\) *def ',line):

        newline = re.sub(r'\~\) *','',line)
        functions = newline.split('{|')

        for s in functions:
            newFunctions.append(re.sub(r' *\|\} *','',s))

        def_match = "\n".join(newFunctions) + "\n\n"

    if re.search(r'error',line):
        res_error += def_match
    else:
        res_functions += def_match

    return i, res_error, res_functions


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE YACC
def translate_yacc(lines: List[str]):
    
    pos = 0

    res = ""
    res_functions = ""
    dictionary = ""
    res_error = ""
    about_parser = ""
    prec = "" 
    grammar = []

    while pos < len(lines):
        
        # process grammar
        if re.match(r'^/grammar$',lines[pos]):
            for subline in lines[pos+1:]:
                if re.match(r'\w+ : .*',subline):
                    grammar.append(subline)
                    pos = pos + 1
                else: break
            pos = pos + 1                               # avançar a última posição da gramática e a linha %%

        # process yacc parser
        elif re.match(r'/% *.*',lines[pos]):                      # não é uma variável, mas é uma linha importante que deve ser escrita no yacc
            about_parser += (re.findall(r'(?:\/\% *(.*))',lines[pos]))[0] + "\n"

        # process precendence variable if exists
        elif re.search(r'%[a-z][A-Za-z]*\s?=\s?\[.*\];',lines[pos]):
            newline = re.sub(r'% *|;','',lines[pos])
            prec += newline
            """
            precedence.append(newline)
            for subline in lines[lines.index(lines[pos])-len(lines)+1:]:
                if re.search(r'\s*\(.*\),|\]',subline):
                    precedence.append(subline)
                else: break
            """

        # if dictionary exists
        elif re.search(r'%.*= *\{\}',lines[pos]):
            dictionary = (lines[pos])[lines[pos].index("%")+len("%"):] + "\n\n"

        # process functions -- def
        pos, res_error, res_functions = process_function(lines[pos], pos, res_error, res_functions)
        pos = pos + 1

    defGrammar, res_grammar = process_grammar(grammar)
    res += "\n".join(defGrammar) + "\n\n" + prec + "\n\n"

    # a função de error tem de aparecer depois das funções da gramática
    res += dictionary + res_functions + res_grammar + res_error + about_parser

    return res

# CRIA E ESCREVE NO FILE YACC
def write_file_yacc(input_name:str, res0: str):

    input_name = re.sub(r'\.(.*)',r'',input_name)

    imports = f"""import ply.yacc as yacc\nfrom {input_name}_lex import *"""
    res = imports + "\n\n" + res0

    outputFile = open("../output/"+f'{input_name}_yacc.py','w')
    outputFile.write(res)
    outputFile.close

    print("\033[96m[" + input_name + "]\033[92m translated YACC successfully.\033[0m")