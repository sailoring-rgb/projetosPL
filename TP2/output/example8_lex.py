import ply.lex as lex

tokens = ['num', 'id', 'DUMP','FIM']  
t_ignore = " \t\n"
t_id = r'[_A-Za-z]\w*'
t_DUMP = r'!!'
t_FIM = r'\.'

def t_num(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
