import ply.lex as lex

## LEX
literals = "+-/*=()"                ## a single char
tokens = ['VAR', 'NUMBER']

t_ignore = "\t\n"

def t_VAR(t):
    r'[_A-Za-z][_0-9A-Za-z]*'
    t.value = t.value
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

"""
def t_UMINUS(t):
    r'-\d+(\.\d+)?'
    return t
"""

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()