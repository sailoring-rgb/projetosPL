import re
import sys
from typing import List

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

lines = open_file()
lines_for_LEX, lines_for_YACC = lex_or_yacc(lines)

"""
print("-------------------------------------FOR LEX---------------------------------------------")
for line in lines_for_LEX:
    print(line)
print("-------------------------------------FOR YACC---------------------------------------------")
for line in lines_for_YACC:
    print(line)
"""