from ast import parse
import ply.yacc as yacc
from plySimple_lex import tokens
from helper import *

"""
    PlySimple : BLEX Lex BYACC Yacc EOF
    Lex : Vars Funs
    Vars : Vars Var
         |
    Var : LIT literals
         | IGN ig
         | TOK tokenList
    Funs : Funs Fun
         |
    Fun : BFUN function
    Yacc : Precedence Dictionary Grammar Defs InstrList
    Dictionary : TS tsList
               |
    Grammar : BGRAM ProdList
            |
    ProdList : ProdList prod
             |
    Defs : Defs Def
         |
    Def : BDEF definition
    InstrList : InstrList Inst
              |
    Inst : BINST instruction
"""

# Production rules
def p_PlySimple(p):
    'PlySimple : BLEX Lex BYACC Yacc EOF'

def p_Yacc(p):
    'Yacc : Precedence Dictionary Grammar Defs InstrList'

def p_Precedence(p):
    'Precedence : PREC preceList'

def p_Precedence_Empty(p):
    'Precedence : '

def p_Dictionary(p):
    'Dictionary : TS tsList'

def p_Dictionary_Empty(p):
    'Dictionary : '

def p_Grammar(p):
    'Grammar : BGRAM ProdList'

def p_Grammar_Empty(p):
    'Grammar : '

def p_ProdList(p):
    'ProdList : ProdList prod'

def p_ProdList_Empty(p):
    'ProdList : '

def p_Defs(p):
    'Defs : Defs Def'

def p_Defs_Empty(p):
    'Defs : '
 
def p_Def(p):
    'Def : BDEF definition'

def p_InstrList(p):
    'InstrList : InstrList Inst'

def p_InstrList_Empty(p):
    'InstrList : '

def p_Inst(p):
    'Inst : BINST instruction'

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
    'Fun : BFUN function'

def p_error(p):
    print("ERROR", p)
    parser.success = False
    exit(1)

# Build the parser
parser = yacc.yacc()

# Definir estado / modelo
parser.state = {}

import sys
files = sys.argv[1:]

for file_name in files:
    try:
        f = open("../input/"+file_name, 'r')
        input = f.read()
    except FileNotFoundError:
        input = ""
        print("\033[91m[ERROR] file "+ file_name + " not found.\033[0m")
    if input != "":
        parser.success = True
        parser.parse(input)
        if parser.success:
            print("###### END YACC PROCESSING ######")