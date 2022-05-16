import ply.yacc as yacc
from plySimple_lex import tokens
from helper import *

# Production rules
def p_plySimple_BLEX(p):
    "Ply-Simple : Lex EOF"

def p_Lex(p):
    'Lex : BLEX Vars Funs'

def p_Vars_notEmpty(p):
    'Vars : Vars Var'

def p_Vars_Empty(p):
    'Vars : '

def p_Var_Literals(p):
    "Var : LIT literals"

def p_Var_Ignore(p):
    "Var : IGN ig"

def p_Var_ListTok(p):
    "Var : TOK tokenList"

def p_Funs_notEmpty(p):
    "Funs : Funs Fun EFUNL"

def p_Funs_Empty(p):
    "Funs : "

def p_Fun(p):
    "Fun : BFUNL funL"

def p_error(p):
    print("ERROR",p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Definir estado / modelo
parser.info = {}

## PARSING TO EVENTUALLY MOVE TO YACC
import sys
files = sys.argv[1:]

for file_name in files:
    f = open("../input/"+file_name) 
    for line in f:
        parser.success = True
        parser.parse(line)
        if parser.success:
            print('Frase válida: ', line)