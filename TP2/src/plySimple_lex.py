import ply.lex as lex

tokens = ['LIT','TOK', 'IGN','ERR','BLEX','RET']
states = [("lex", 'inclusive'),
          ("yacc", 'inclusive')]

t_ignore = " \t\n"

def t_BLEX(t):
    r'%% *LEX'
    t.lexer.begin("lex")
    return t 

def t_YACC(t):
    r'%% *YACC'
    t.lexer.begin("yacc")
    return t 

def t_lex_TOK(t):
    r'% *tokens'
    t.lexer.forLEX = t.lexer.forLEX.append(t.value)
    return t

def t_LIT(t):
    r'% *literals *='
    return t

def t_TOK(t):
    r'% *tokens'
    return t

def t_ERR(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

def t_IGN(t):
    r' \t\n'
    return t

def t_RET(t):
    r'% *return'
    return t

def t_EOF(t):
    r'$'
    return t

lexer = lex.lex()
lexer.forLEX = []
lexer.forYACC = []

import sys
# cat text.txt | python3.10 ex2.py
f = open("../input/example1.txt")
for line in f:
    lexer.input(line)
print("\n\nEncontrei " + "\n".join(lexer.forLEX))