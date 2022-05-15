import re
from typing import List


###################################################### EXCEPTIONS ######################################################
class GrammarError(Exception):
    """Raised when no grammar is defined"""
    pass

class VariableError(Exception):
    """Raised when variables are missing or not correctly introduced"""
    pass
#######################################################################################################################


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
        if re.search(r'%% *LEX',line):
            pos_lex = pos                   # pos em que começa o conteúdo para o file lex
            lex_exists = True
        if re.search(r'%% *YACC',line):
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


# ABRE UM FICHEIRO E DEVOLVE UMA LISTA COM O SEU CONTEÚDO
def open_file(input_name:str):
    file = open("../input/"+input_name)
    
    if not file:
        raise FileNotFoundError

    lines = file.read().splitlines()
    file.close()
    print("\033[96m[" + input_name[:-4] + "]\033[0m\033[92m opened successfully.\033[0m")
    return lines


# CRIA E ESCREVE NO FILE LEX
def write_file_lex(input_name:str, res0: str):

    imports = "import ply.lex as lex"
    res = imports + "\n\n" + res0

    input_name = re.sub(r'\.(.*)',r'',input_name)
    outputFile = open("../output/"+f'{input_name}_lex.py','w')
    outputFile.write(res)
    outputFile.close

    print("\033[96m[" + input_name + "]\033[92m translated LEX successfully.\033[0m")


# CRIA E ESCREVE NO FILE YACC
def write_file_yacc(input_name:str, res0: str):

    input_name = re.sub(r'\.(.*)',r'',input_name)

    imports = f"""import ply.yacc as yacc\nfrom {input_name}_lex import *"""
    res = imports + "\n\n" + res0

    outputFile = open("../output/"+f'{input_name}_yacc.py','w')
    outputFile.write(res)
    outputFile.close

    print("\033[96m[" + input_name + "]\033[92m translated YACC successfully.\033[0m")