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
