import ply.lex as lex

tokens = ['num','FIM']
tokens = ['num','FIM']
t_ignore = " \t\n"
t_FIM = r'\.'

def t_num(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_error(t):
    print(f"Caracter ilegal: , {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
