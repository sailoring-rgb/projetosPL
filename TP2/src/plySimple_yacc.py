from ast import parse
import ply.yacc as yacc
from plySimple_lex import tokens
from helper import *

"""
    PlySimple : BLEX Lex
    Lex : Vars Funs
    Vars : Vars Var
         |
    Var : LIT literals
         | IGN ig
         | TOK tokenList
    Funs : Funs Fun
         |
    Fun : BFUNL funL
"""

# Production rules

def p_PlySiple(p):
    'PlySimple : BLEX Lex EOF'

def p_Lex(p):
    'Lex : Vars Funs'

def p_Vars(p):
    'Vars : Vars Var'

def p_Vars_Empty(p):
    'Vars : '

def p_Var_Literals(p):
    'Var : LIT literals'

def p_Var_Ignore(p):
    'Var : IGN literals'

def p_Var_ListTok(p):
    'Var : TOK tokenList'

def p_Funs(p):
    'Funs : Funs Fun'

def p_Funs_Empty(p):
    'Funs : '

def p_Fun(p):
    'Fun : BLFUN funL '

def p_error(p):
    print("ERROR",p)
    parser.success = False
    exit(1)

# Build the parser
parser = yacc.yacc()

# Definir estado / modelo
parser.state = {}

import sys
files = sys.argv[1:]

for file_name in files:
    f = open("../input/"+file_name, 'r')
    parser.success = True
    parser.parse(f.read())
    if parser.success:
        print("###### END YACC PROCESSING ######")