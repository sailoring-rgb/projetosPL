import ply.lex as lex

tokens = ['PLUS','MINUS','SEPARATOR','NUM']
t_ignore = '\n\t '

def t_PLUS(t):
    r'\+'
    t.lexer.begin("state1")
    return t

def t_state1_PLUS(t):
    r'\+'
    t.lexer.begin("INITIAL")
    return t

def t_SEPARATOR(t):
    r','
    return t

def t_state1_NUM(t):
    r'\d+'
    t.lexer.soma+=int(t.value)
    return t

def t_NUM(t):
    r'\d+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
lexer.soma = 0
