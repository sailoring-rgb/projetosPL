from ast import arg
import ply.lex as lex
from helper import *

tokens = [
    'BLEX',
    'EOF',
    'LIT',
    'IGN',
    'TOK',
    'literals',
    'literalsV2',
    'tokenList',
    'BFUN',
    'function',
    'BDEF',
    'definition',
    'BYACC',
    'PREC',
    'preceList',
    'TS',
    'tsList',
    'BGRAM',
    'prod',
    'BINST',
    'instruction'
    ]

states = [
    ("lex", 'exclusive'),
    ("fun", 'exclusive'),
    ("yacc", 'exclusive'),
    ("grammar", 'exclusive'),
    ("def", 'exclusive'),
    ("parser", 'exclusive')
    ]

t_ANY_ignore = " \t\n"

def t_ANY_EOF(t):
    r'\$\$'
    return t

def t_ANY_BINST(t):
    r'/%'
    t.lexer.begin("parser")
    return t

def t_parser_instruction(t):
    r'.*(\.|\=|\w+).*'
    t.lexer.begin("INITIAL")
    return t

def t_ANY_BYACC(t):
    r'%%\s*YACC\s*%%'
    t.lexer.begin("yacc")
    return t

def t_yacc_PREC(t):
    r'%\s*precedence\s*=\s*'
    return t

def t_yacc_preceList(t):
    r'\[\(.*\)\];'
    return t

def t_yacc_TS(t):
    r'%\s*ts\s*=\s*'
    return t

def t_yacc_tsList(t):
    r'\{\}'
    return t

def t_ANY_BGRAM(t):
    r'/grammar'
    t.lexer.begin("grammar")
    return t

def t_grammar_prod(t):
    r'.*\:.*\{.*\}'
    return t

def t_ANY_BLEX(t):
    r'%%\s*LEX\s*%%'
    t.lexer.begin("lex")
    return t

def t_lex_TOK(t):
    r'%\s*tokens\s*=\s*'
    return t

def t_lex_tokenList(t):
    r'\[\'*.*\'\]'
    return t

def t_lex_LIT(t):
    r'%\s*literals\s*=\s*'
    return t

def t_lex_literals(t):
    r'\".*\"'
    return t

def t_lex_literalsV2(t):
    r'\'.*\''
    return t

def t_lex_IGN(t):
    r'%\s*ignore\s*=\s*'
    return t

def t_ANY_BFUN(t):
    r'\s*%\)\s*'
    t.lexer.begin("fun")
    return t

def t_fun_function(t):
    r'.*(return|error|simpleToken).*'
    t.lexer.begin("INITIAL")
    return t

def t_ANY_BDEF(t):
    r'\~\)'
    t.lexer.begin("def")
    return t

def t_def_definition(t):
    r'def\s*\w+\(\w+\)\: \s*\{\|\s.* \|\}'
    return t

def t_ANY_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()

# In case some testing might be needed
"""
import sys
files = sys.argv[1:]

for file_name in files:
    try:
        lines = open_file(file_name, 'LEX')
    except FileNotFoundError:
        lines = ''
        print("\033[91m[ERROR] file "+ file_name + " not found.\033[0m")
    for line in lines:
        lexer.input(line)
        for tok in lexer:
            print(tok)
    print("###### END LEX PROCESSING ######")
"""