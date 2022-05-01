import re
from typing import List


# PROCESSA A GRAMÁTICA RECEBIDA E DEVOLVE UMA STRING COM TODAS AS FUNÇÕES PARA O FILE YACC
def process_grammar(grammar: List[str]):
    i = 1
    res_grammar = ""
    defGrammar = ["# GRAMMAR:"]

    for line in grammar:
        if line != "":
            group = (re.findall(r'([^: ]+)(?: *: *(.*?) {2,})(?:{ *(.*?) *})',line))[0]

            # process a production of grammar
            prod = re.sub(r'( %.*)','',group[1])     # remover, por exemplo, %prec UMINUS
            op = re.findall(r'(.*?[^A-Za-z]?)([A-Za-z])(\[\d+\]\)?)',group[2])

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
def process_function(lines: List[str], line: str, i: int, res_functions: str):

    function = []
    if re.match(r'def ',line):
        function.append(line)
        f = i + 1
        for s in lines[i+1:]:
            if re.match(r'  ',s):
               function.append(s)
            else: break
            f = f + 1
        res_functions += "\n".join(function) + "\n\n"
        i = f - 1
    else: i = i + 1

    return i, res_functions


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE YACC
def translate_yacc(lines: List[str]):
    
    content = "\n".join(lines)           # converte a lista com as linhas para o yacc numa string
    res = ""

    grammar = content[content.index("{}") + len("{}"):content.index("%%") + len("%%")-2]      # pega nas linhas destinadas à gramática
    defGrammar, res_grammar = process_grammar(grammar.split("\n"))
    res += "\n".join(defGrammar) + "\n\n"                                                       # construir a gramática em comentários

    i = 0
    res_functions = ""
    precedence = []
    for line in lines:

        if re.match(r'%\w+\s?=\s?\[.*',line):
            newline = re.sub(r'%','',line)
            precedence.append(newline)
            for s in lines[lines.index(line)-len(lines)+1:]:
                if re.search(r'\s*\(.*\),|\]',s):
                    precedence.append(s)
                else: break

        i, res_functions = process_function(lines, line, i, res_functions)

        parser_match = re.findall(r'([^ \.])(?:\.parse\((.*?)\))',line)       # grupo 1 - nome da var. # grupo 2 - conteúdo do parse

    res += "\n".join(precedence) + "\n\n"

    dictionary = (re.findall(r'.*\{\}',content))[0]
    res += dictionary + "\n\n" + res_grammar + res_functions

    res += f"""{parser_match[0][0]} = yacc.yacc()
{parser_match[0][0]}.parse({parser_match[0][1]})"""

    return res