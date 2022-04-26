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