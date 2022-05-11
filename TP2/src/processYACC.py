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
    {calc}\n\n"""
            i = i+1
    
    return defGrammar, res_grammar


# PROCESSA UMA FUNÇÃO DESTINADA AO FILE YACC
def process_function(lines: List[str], line: str, i: int, res_functions: str):

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

    return i, def_match


# DEVOLVE UMA LISTA COM O CONTEÚDO TRADUZIDO PARA O FILE YACC
def translate_yacc(lines: List[str]):
    
    content = "\n".join(lines)           # converte a lista com as linhas para o yacc numa string
    res = ""

    if "/%" in content and "%%" in content:
        grammar = content[content.index("/%") + len("/%"):content.index("%%") + len("%%")-2]        # pega nas linhas destinadas à gramática
        defGrammar, res_grammar = process_grammar(grammar.split("\n"))
        res += "\n".join(defGrammar) + "\n\n"                                                       # construir a gramática em comentários
    else:
        raise GrammarError

    i = -1
    pos = 0
    res_functions = ""
    dictionary = ""
    res_error = ""
    about_parser = ""
    precedence = []
    
    for line in lines:

        if pos > i:
            # process precendence variable if exists
            if re.search(r'\w+\s?=\s?\[.*',line):
                if re.match(r'% *',line):
                    newline = re.sub(r'% *','',line)
                    precedence.append(newline)
                    for s in lines[lines.index(line)-len(lines)+1:]:
                        if re.search(r'\s*\(.*\),|\]',s):
                            precedence.append(s)
                        else: break
                else:
                    raise VariableError

            i, def_match = process_function(lines, line, pos, res_functions)
            if re.search(r'error',line):
                res_error = def_match
            else:
                res_functions += def_match

            if re.search(r'.*= *\{\}',line):
                dictionary = line + "\n\n"

            # exemplo =                 y.parse("3+4*7")
            # primeiro termo =          y
            # segundo tempo =           "3+4*7"
            if re.match(r'\/%',line):                      # não é uma variável, mas é uma linha importante que deve ser escrita no lex
                about_parser += line[line.index("/%")+len("/%"):] + "\n"
        else:
            pass
        pos = pos + 1

    res += "\n".join(precedence) + "\n\n"

    res += dictionary + res_functions + res_grammar + res_error        # a função de error tem de aparecer depois das funções da gramática

    res += about_parser

    return res
