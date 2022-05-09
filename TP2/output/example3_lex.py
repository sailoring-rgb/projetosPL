import ply.lex as lex

tokens = ['INI','FIM','nome','real','int','sinal']
sinal = '[=+\-*/()]'
t_ignore = " \n\t"

def t_INI(t):
    r'(?:begin)|\{'
    return t

def t_FIM(t):
    r'\}|[eE] [nN] [dD]'
    return t

def t_nome(t):
    r'[a-zA-Z] [a-zA-Z0-9]*'
    return t

def t_real(t):
    r'[0-9]+\.[0-9]+'
    return t

def t_int(t):
    r'[0-9]+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
