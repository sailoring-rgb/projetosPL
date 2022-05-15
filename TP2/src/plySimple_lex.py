import ply.lex as lex

tokens = ['LIT','TOK', 'IGN','BLEX','RET','ERR','EOF','NLINE','VIRG','TAB','SEP','SEP1','SEP2','BYACC']
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

def t_lex_tok(t):
    r'\".*\"'
    t.lexer.forLEX.append(t.value)
    
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

def t_yacc_VIRG(t):
    r'\,'
    t.lexer.forYACC.append(t.value)
    return t 

def t_yacc_SEP(t):
    r'\-'
    t.lexer.forYACC.append(t.value)
    return t 

def t_yacc_SEP1(t):
    r'\-\-'
    t.lexer.forYACC.append(t.value)
    return t 

def t_yacc_SEP2(t):
    r'\-\-\-'
    t.lexer.forYACC.append(t.value)
    return t 

def t_yacc_TAB(t):
    r'  '
    t.lexer.forYACC.append(t.value)
    return t 

def t_yacc_NLINE(t):
    r'\n'
    t.lexer.forYACC.append(t.value)
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
f = open("example1.txt")
for line in f:
    lexer.input(line)
    for tok in lexer:
        print(tok)
print("\n\nEncontrei " + "\n".join(lexer.forLEX))