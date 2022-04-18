import re
from typing import List


# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def get_lex_yacc(lines: List[str]):

    pos = 0
    lines_for_LEX = []              # guarda todo o conteúdo para o file lex
    lines_for_YACC = []             # guarda todo o conteúdo para o file yacc

    # saber em que posição começa o conteúdo para o file lex
    # e em que posição começa o conteúdo para o file yacc
    for line in lines:
        if re.search(r'LEX',line):
            pos_lex = pos
        if re.search(r'YACC',line):
            pos_yacc = pos
        pos = pos + 1

    for line in lines[pos_lex+1:pos_yacc]:
        lines_for_LEX.append(line)
    
    for line in lines[pos_yacc+1:]:
        lines_for_YACC.append(line)
    
    return lines_for_LEX, lines_for_YACC


# DEVOLVE UMA STRING COM A DEFINIÇÃO DA FUNÇÃO PARA O FILE LEX
def lex_function(tok: str, regex: str, t, type: str):

    tok = re.sub(r'\'',r'',tok)
    if type == "float":
        res = f"""def t_{tok}(t):
    r'{regex}'
    t.value = float(t.value)
    return t\n"""
    elif type == "int":
        res = f"""def t_{tok}(t):
    r'{regex}'
    t.value = int(t.value)
    return t\n"""
    elif type == "str":
        res = f"""def t_{tok}(t):
    r'{regex}'
    return t\n"""
    return res


# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def translate_lex(lines_for_lex: List[str]):

    res = "\n"

    tokens_match = [s for s in lines_for_lex if "tokens" in s][0]                     #string: tokens_match = "tokens = [ 'VAR', 'NUMBER' ]"
    tokens = (re.findall(r'(?:\[\s?)(.*)(?:\s?\])', tokens_match)[0]).split(",")      #list: tokens = ["'VAR'", "'NUMBER'"]

    list_returns = [s for s in res if "return" in s]

    for tok in tokens:
        tok = re.sub(r'\s+',r'',tok)
        for s in list_returns:
            if tok in s:
                regex = re.findall(r'^(.*)(?:return)',s)[0]
                regex = re.sub(r' +$','',regex)
                regex = re.sub(r'\\{2}',r'\\',regex)

                if re.match(f'{regex}',"1.0"):
                    type = "float"
                elif re.match(f'{regex}',"1"):
                    type = "int"
                else:
                    type = "str"
                res = res + lex_function(tok,regex,"t",type)
            else: pass


# ABRE UM FICHEIRO E DEVOLVE UMA LISTA COM O SEU CONTEÚDO
def open_file():
    file_name = input("[CSV] Insert file name (extension included): ")

    try:	
        file = open("../input/"+file_name)
    except OSError:
        print(f"[ERROR] Can't locate CSV file \"{file_name}\".\n")
        input("[PRESS ENTER TO CONTINUE]")
        return -1

    if file:
        lines = file.read().splitlines()
        print("[FILE] Opened successfully.")
        input("[PRESS ENTER TO CONTINUE]")
        file.close()
        return lines