import ply.lex as lex

literals = ['[',']']
tokens = ['id','num']
t_ignore = " \t\n"
t_id = r'\"[^'']+\"'

def t_num(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
