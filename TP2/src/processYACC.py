from cgitb import reset
import re
from typing import List


# PROCESSA A GRAMÁTICA RECEBIDA E DEVOLVE UMA STRING COM TODAS AS FUNÇÕES PARA O FILE YACC
def process_grammar(grammar: List[str]):
    i = 1
    res = ""
    for line in grammar:
        if line != "":
            group = (re.findall(r'([^: ]+)(?: *: *(.*?) {2,})(?:{ *(.*?) *})',line))[0]
            # process a production of grammar
            prod = re.sub(r'( %.*)','',group[1])
            res += f"""def p_{group[0]}_p{i}:
    "{group[0]} : {prod}"
    {group[2]}\n\n"""
            i = i+1
        else: pass
    
    return res


# PROCESSA UMA FUNÇÃO DESTINADA AO FILE YACC
def process_function(lines: List[str], line: str, i: int, res: str):

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

    return i, res


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE YACC
def translate_yacc(lines: List[str]):
    
    content = "\n".join(lines)           # converte a lista com as linhas para o yacc numa string
    res = ""

    dictionary = (re.findall(r'.*\{\}',content))[0]
    res += dictionary + "\n\n"

    grammar = content[content.index("{}") + len("{}"):content.index("%%") + len("%%")-2]
    res += process_grammar(grammar.split("\n"))

    i = 0
    for line in lines:

        i, res = process_function(lines, line, i, res)
        parser_match = re.findall(r'([^ \.])(?:\.parse\((.*?)\))',line)       # grupo 1 - nome da var. # grupo 2 - conteúdo do parse

    res += f"""{parser_match[0][0]} = yacc.yacc()
{parser_match[0][0]}.parse({parser_match[0][1]})"""

    return res


