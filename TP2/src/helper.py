import re
import sys
from typing import List


# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def lex_or_yacc(lines: List[str]):

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

"""
# DEVOLVE UMA LISTA COM O CONTEÚDO DO FILE LEX E OUTRA LISTA COM O CONTEÚDO DO FILE YACC
def translate_lex(lines_for_lex: List[str]):

    res = "\n"
    for line in lines_for_lex:
        if re.search(r'tokens',line):
            content = line[line.index("tokens") + len("tokens"):]
            res = res + "tokens" + content + "\n"
        if re.search(r'ignore',line):
            content = line[line.index("ignore") + len("ignore"):]
            res = res + "t_ignore" + content + "\n"
    print(res)
"""

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