from ast import arg
import ply.lex as lex
from helper import *

tokens = [
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
    'instructions',
    'BCOM',
    'ECOM',
    'comm'
    ]

states = [
    ("lex", 'inclusive'),
    ("lexFun", 'inclusive'),
    ("yacc", 'inclusive'),
    ("yaccFun", 'inclusive'),
    ("grammar", 'inclusive'),
    ("parser", 'inclusive'),
    ("comment", 'inclusive')
    ]

t_ANY_ignore = " \t\n"

### TREATING COMMENTS ###
def t_ANY_BCOM(t):
    r'\<\#\>'
    t.lexer.begin("comment")
    return t

def t_ANY_ECOM(t):
    r'\>\#\<'
    t.lexer.begin("INITIAL")
    return t

def t_comment_comm(t):
    r'(:?\s*:?[A-z]+:?\s*)+'
    return t

### PARSER INFORMATION AND INSTRUCTIONS ###
def t_yacc_BPARSER(t):
    r'%%\s*PARSER\s*%%'
    t.lexer.begin("parser")
    return t

def t_parser_instructions(t):
    r'.*parse(.*).*'
    t.lexer.forParser.append(t.value)
    return t

### YACC SECTION ###
def t_ANY_BYACC(t):
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

### GRAMMAR ###
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

### YACC FUNCTIONS ###
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

### LEX SECTION ###
def t_ANY_BLEX(t):
    r'%%\s*LEX\s*%%'
    t.lexer.begin("lex")
    return t

def t_lex_LIT(t):
    r'%\s*literals\s*=\s*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_literals(t):
    r'\".*\"'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_IGN(t):
    r'%\s*ignore\s*=\s*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_ig(t):
    r'\".*\"'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_TOK(t):
    r'%\s*tokens\s*=\s*'
    t.lexer.forLEX.append(t.value)
    return t

def t_lex_tokenList(t):
    r'\[(\'*.*\')+\]'
    t.lexer.forLEX.append(t.value)
    return t

### LEX FUNCTIONS ###
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

### ERRO FUNCTION ###
def t_ANY_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()

## LEX VARIABLES TO REMOVE 
lexer.forLEX = []
lexer.forLEXfun = []
lexer.forYACC = []
lexer.forYACCgram = []
lexer.forYACCfun = []
lexer.forParser = []


## PARSING TO EVENTUALLY MOVE TO YACC
import sys
files = sys.argv[1:]

for file_name in files:
    try:
        lines = open_file(file_name)
    except FileNotFoundError:
        lines = ''
        print("\033[91m[ERROR] file "+ file_name + " not found.\033[0m")
    for line in lines:
        lexer.input(line)
        for tok in lexer:
            print(tok)
    print("###### END LEX PROCESSING ######")
