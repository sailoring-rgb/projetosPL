from cgitb import reset
import re
from typing import List


# PROCESSA A GRAMÁTICA RECEBIDA E DEVOLVE UMA STRING COM TODAS AS FUNÇÕES PARA O FILE YACC
def process_grammar(res: str, grammar: List[str]):
    i = 1
    for line in grammar:
        group = re.findall(r'([^: ]+)(?: *: *(.*?) {2,})(?:{ *(.*?) *})',line)
        
        # process a function for the yacc file
        prod = re.sub(r'( %.*)','',group[0][1])
        res += f"""def p_{group[0][0]}_p{i}:
    "{group[0][0]} : {prod}"
    {group[0][2]}\n\n"""
        i = i+1
    
    return res


# PROCESSA UMA FUNÇÃO DESTINADA AO FILE YACC
def process_function(lines: List[str]):

    res = ""
    i = 0
    f = -1

    for line in lines:
        function = []
        if re.match(r'def ',line):
            function.append(line)
            f = i+1
            for s in lines[i+1:]:
                if re.match(r'  ',s):
                   function.append(s)
                else: break
                f = f + 1
            res += "\n".join(function) + "\n\n"
            i = f - 1
        else: i = i + 1

    return res


def translate_yacc(lines: List[str]):
    
    text = "\n".join(lines)           # converte a lista com as linhas para o yacc numa string
    res = ""

    dictionary = (re.findall(r'.*\{\}',text))[0]
    res += dictionary + "\n\n"

    res += process_function(lines)

translate_yacc(ex)