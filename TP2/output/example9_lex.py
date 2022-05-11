import ply.lex as lex

tokens = ['Z', 'U']
t_ignore = " \t\n"
t_Z = r'0'
t_U = r'1'

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
