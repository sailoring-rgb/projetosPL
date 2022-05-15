import ply.lex as lex

tokens = ['TOK', 'IGNORE', 'ERROR', 'VAR']
states = [("lex", 'inclusive'),
          ("yacc", 'inclusive')]

t_ignore = " \t\n"

def t_LEX(t):
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

def t_TOK(t):
    r'% *tokens'
    return t

def t_ERROR(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

def t_VAR(t):
    r'[_A-Za-z][_0-9A-Za-z]*'
    return t

lexer = lex.lex()
lexer.forLEX = []
lexer.forYACC = []