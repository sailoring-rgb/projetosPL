import ply.lex as lex

tokens = ['PA', 'PF', 'NUM', 'VIRG']
t_ignore = " \t\n"
t_PA = r'\)'
t_PF = r'\('
t_NUM = r'\d+'
t_VIRG = r'\,'

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
