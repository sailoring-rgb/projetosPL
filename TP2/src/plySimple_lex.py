import ply.lex as lex

tokens = ['LIT','TOK', 'IGN','BLEX','RET','ERR','EOF']
states = [("lex", 'inclusive'),
          ("yacc", 'inclusive')]

t_ignore = " \t\n"

def t_BLEX(t):
    r'%%\s*LEX\s*%%'
    print("found")
    t.lexer.begin("lex")
    return t 
"""
def t_BYACC(t):
    r'%% *YACC'
    t.lexer.begin("yacc")
    return t 
"""
def t_lex_TOK(t):
    r'% *tokens *=.*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_LIT(t):
    r'% *literals *=.*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_IGN(t):
    r'% *ignore *=.*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_RET(t):
    r'% *return.*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_ERR(t):
    # r'(?:.*?error\((.*)(?:\)))'
    r'.*?error'
    t.lexer.forLEX.append(t.value)
    return t

def t_ANY_EOF(t):
    r'\$'
    t.lexer.forLEX.append(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
lexer.forLEX = []
lexer.forYACC = []

import sys
# cat text.txt | python3.10 ex2.py
f = open("../old/input/example1.txt")
for line in f:
    print(line)
    lexer.input(line)
print("\n\nEncontrei " + "\n".join(lexer.forLEX))