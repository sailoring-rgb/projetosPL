import ply.lex as lex

tokens = [
    'EOF',
    'BLEX',
    'LIT',
    'IGN',
    'TOK',
    'literals',
    'ig',
    'tokenList',
    'BFUNL',
    'EFUNL',
    'funL',
    'BYACC',
    'PREC',
    'preceList',
    'TS',
    'tsList',
    'BGRAM',
    'EGRAM',
    'gram',
    'EFUNY',
    'BFUNY',
    'funY',
    'BPARSER',
    'instructions'
    ]

states = [
    ("lex", 'inclusive'),
    ("lexFun", 'inclusive'),
    ("yacc", 'inclusive'),
    ("yaccFun", 'inclusive'),
    ("grammar", 'inclusive'),
    ("parser", 'inclusive')
    ]

t_ignore = " \t\n"

def t_ANY_EOF(t):
    r'\$\$'
    t.lexer.forLEX.append(t.value)
    return t

def t_BPARSER(t):
    r'%%\s*PARSER\s*%%'
    t.lexer.begin("parser")
    return t

def t_parser_instructions(t):
    r'.*parse(.*).*'
    t.lexer.forParser.append(t.value)
    return t


def t_BYACC(t):
    r'%%\s*YACC\s*%%'
    t.lexer.begin("yacc")
    return t

def t_yacc_PREC(t):
    r'%\s*precedence\s*=\s*'
    t.lexer.forYACC.append(t.value)
    return t

def t_yacc_preceList(t):
    r'\[\(.*\]'
    t.lexer.forYACC.append(t.value)
    return t

def t_yacc_TS(t):
    r'%\s*ts\s*=\s*'
    t.lexer.forYACC.append(t.value)
    return t

def t_yacc_tsList(t):
    r'\{\}'
    t.lexer.forYACC.append(t.value)
    return t

def t_yacc_BGRAM(t):
    r'/%\\'
    t.lexer.begin("grammar")
    return t

def t_grammar_EGRAM(t):
    r'/%%\\'
    t.lexer.begin("yacc")
    return t

def t_grammar_gram(t):
    r'(.*\{.*\})'
    t.lexer.forYACCgram.append(t.value)
    return t

def t_yacc_EFUNY(t):
    r'%\)'
    t.lexer.begin("yaccFun")
    return t

def t_yaccFun_EFUNY(t):
    r'\(%'
    t.lexer.begin("yacc")
    return t

def t_yaccFun_funY(t):
    r'def .*'
    t.lexer.forYACCfun.append(t.value)
    return t

def t_BLEX(t):
    r'%%\s*LEX\s*%%'
    t.lexer.begin("lex")
    return t

def t_lex_LIT(t):
    r'%\s*literals\s*=\s*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_IGN(t):
    r'%\s*ignore\s*=\s*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_TOK(t):
    r'%\s*tokens\s*=\s*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_BFUNL(t):
    r'%\)'
    t.lexer.begin("lexFun")
    return t

def t_lexFun_EFUNL(t):
    r'\(%'
    t.lexer.begin("lex")
    return t

def t_lexFun_funL(t):
    r'(.*(return|error).*)'
    t.lexer.forLEXfun.append(t.value)
    return t

def t_lex_literals(t):
    r'\".*\"'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_ig(t):
    r'\".*\"'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_tokenList(t):
    r'\[(\'*.*\')+\]'
    t.lexer.forLEX.append(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
lexer.forLEX = []
lexer.forLEXfun = []
lexer.forYACC = []
lexer.forYACCgram = []
lexer.forYACCfun = []
lexer.forParser = []

import sys
f = open("example1.txt")
for line in f:
    lexer.input(line)
    for tok in lexer:
        print(tok)
print("\n\nEncontrei\n " + "\n".join(lexer.forParser))