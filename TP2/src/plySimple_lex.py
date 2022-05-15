import ply.lex as lex

tokens = ['LIT','TOK', 'IGN','BLEX','RET','ERR','EOF']
states = [("lex", 'inclusive'),
          ("yacc", 'inclusive')]

t_ignore = " \t\n"

def t_BLEX(t):
    r'%% *LEX'
    t.lexer.begin("lex")
    return t 
"""
def t_BYACC(t):
    r'%% *YACC'
    t.lexer.begin("yacc")
    return t 
"""
def t_lex_TOK(t):
    r'% *tokens *= *'
    t.lexer.forLEX = t.lexer.forLEX.append(t.value)
    return t

def t_lex_LIT(t):
    r'% *literals *= *'
    t.lexer.forLEX = t.lexer.forLEX.append(t.value)
    return t

"""
def t_lex_ERR(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)
"""

def t_lex_IGN(t):
    r'% *ignore *= *'
    t.lexer.forLEX = t.lexer.forLEX.append(t.value)
    return t

def t_lex_RET(t):
    r'% *return'
    t.lexer.forLEX = t.lexer.forLEX.append(t.value)
    return t

def t_EOF(t):
    r'$'
    return t

def t_lex_EOF(t):
    r'$'
    t.lexer.forLEX = t.lexer.forLEX.append(t.value)
    return t

def t_yacc_EOF(t):
    r'$'
    t.lexer.forLEX = t.lexer.forYACC.append(t.value)
    return t

def t_error(t):
    print('Illegal Caracter: ',t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
lexer.forLEX = []
lexer.forYACC = []

import sys
# cat text.txt | python3.10 ex2.py
f = open("../input/example1.txt")
for line in f:
    lexer.input(line)
print("\n\nEncontrei " + "\n".join(lexer.forLEX))