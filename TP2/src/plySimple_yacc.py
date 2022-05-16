from ast import parse
import ply.yacc as yacc
from plySimple_lex import tokens
from helper import *

"""
    PlySimple : Lex EOF
    Lex : BLEX Vars Funs
    Vars : Vars Var
         |
    Var : LIT literals
         | IGN ig"
         | TOK tokenList"
    Funs : Funs Fun EFUNL
         |
    Fun : BFUNL funL
"""

# Production rules
def p_PlySiple_Empty(p):
    'PlySimple : EOF'

def p_PlySiple_notEmpty(p):
    'PlySimple : Lex'

def p_Lex(p):
    'Lex : '
    pass

def p_Lex(p):
    'Lex : BLEX Vars'

def p_Vars_notEmpty(p):
    'Vars : Vars "+" Var'

def p_Vars_Empty(p):
    'Vars : '
    pass

def p_Var_Literals(p):
    'Var : LIT literals'

def p_Var_Ignore(p):
    'Var : IGN ig'

def p_Var_ListTok(p):
    'Var : TOK tokenList'

def p_error(p):
    print("ERROR",p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Definir estado / modelo
parser.info = {}

import sys
files = sys.argv[1:]

for file_name in files:
    try:
        lines = open_file(file_name)
    except FileNotFoundError:
        lines = ''
        print("\033[91m[ERROR] file "+ file_name + " not found.\033[0m")
    for line in lines:
        parser.success = True
        parser.parse(line)
        if parser.success:
            print('Frase válida: ', line)
    print("###### END YACC PROCESSING ######")