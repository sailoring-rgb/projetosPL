import re
from helper import *
from typing import List


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
    {calc}\n"""
            i = i+1
    
    return defGrammar, res_grammar


# PROCESSA UMA FUNÇÃO DESTINADA AO FILE YACC
def process_function(lines: List[str], line: str, i: int, res_error: str, res_functions: str):

    function = []
    def_match = ""

    if re.match(r'def ',line):
        function.append(line)
        f = i + 1
        for s in lines[f:]:
            if re.match(r'  +',s):
               function.append(s)
            else:
                break
            f = f + 1

        def_match = "\n".join(function) + "\n\n"
        i = f - 1

    if re.search(r'error',line):
        res_error += def_match
    else:
        res_functions += def_match

    return i, res_error, res_functions


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE YACC
def translate_yacc(lines: List[str]):
    
    pos = 0
    found_grammar = False

    res = ""
    res_functions = ""
    dictionary = ""
    res_error = ""
    about_parser = ""

    precedence = []
    grammar = []

    while pos < len(lines):
        
        # process grammar
        if re.match(r'^/%$',lines[pos]):
            found_grammar = True
            for subline in lines[pos+1:]:
                if not re.match(r'^%%$',subline):
                    grammar.append(subline)
                    pos = pos + 1
                else: break
            pos = pos + 1                               # avançar a última posição da gramática e a linha %%

        # process yacc parser
        elif re.match(r'/%.*',lines[pos]):                      # não é uma variável, mas é uma linha importante que deve ser escrita no lex
            about_parser += (lines[pos])[lines[pos].index("/%")+len("/%"):] + "\n"

        # process precendence variable if exists
        elif re.search(r'[a-z][A-Za-z]+\s?=\s?\[.*',lines[pos]):
            if re.match(r'% *',lines[pos]):
                newline = re.sub(r'% *','',lines[pos])
                precedence.append(newline)
                for subline in lines[lines.index(lines[pos])-len(lines)+1:]:
                    if re.search(r'\s*\(.*\),|\]',subline):
                        precedence.append(subline)
                    else: break
            else:
                raise VariableError

        # if dictionary exists
        elif re.search(r'.*= *\{\}',lines[pos]):
            dictionary = lines[pos] + "\n\n"

        # process functions -- def
        pos, res_error, res_functions = process_function(lines, lines[pos], pos, res_error, res_functions)

        pos = pos + 1

    if found_grammar == False:
        raise GrammarError
    else:
        defGrammar, res_grammar = process_grammar(grammar)
        res += "\n".join(defGrammar) + "\n\n" + "\n".join(precedence) + "\n\n"

    # a função de error tem de aparecer depois das funções da gramática
    res += dictionary + res_functions + res_grammar + res_error + about_parser

    return res
