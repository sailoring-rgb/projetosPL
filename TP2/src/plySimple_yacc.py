from ast import parse
import ply.yacc as yacc
from plySimple_lex import tokens
from helper import *

"""
    PlySimple : BLEX Lex BYACC Yacc EOF
              | BLEX Lex EOF
              | BYACC Yacc EOF
              | BYACC Yacc BLEX Lex EOF
              | EOF
    Yacc : Precedence Dictionary Grammar Defs InstrList
    Precedence : PREC preceList
               |
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
    Lex : Vars Funs InstrList
    Vars : Vars Var
         |
    Var : LIT Liters
        | IGN Liters
        | TOK tokenList
    Liters : literals
           | literalsV2
    Funs : Funs Fun
         |
    Fun : BFUN function
"""

# Production rules
def p_PlySimple(p):
    'PlySimple : BLEX Lex BYACC Yacc EOF'

def p_PlySimple_LexOnly(p):
    'PlySimple : BLEX Lex EOF'

def p_PlySimple_YaccOnly(p):
    'PlySimple : BYACC Yacc EOF'

def p_PlySimple_ReverseOrder(p):
    'PlySimple : BYACC Yacc BLEX Lex EOF'

def p_PlySimple_Empty(p):
    'PlySimple : EOF'

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
    'Lex : Vars Funs InstrList'

def p_Vars(p):
    'Vars : Vars Var'

def p_Vars_Empty(p):
    'Vars : '

def p_Var_Literals(p):
    'Var : LIT Liters'

def p_Var_Ignore(p):
    'Var : IGN Liters'

def p_Liters(p):
    'Liters : literals'

def p_Liters_V2(p):
    'Liters : literalsV2'

def p_Var_ListTok(p):
    'Var : TOK tokenList'

def p_Funs(p):
    'Funs : Funs Fun'

def p_Funs_Empty(p):
    'Funs : '

def p_Fun(p):
    'Fun : BFUN function'

def p_error(p):
    parser.success = False
    parser.errorLog.append('ERROR : ' + str(p))
    pass

# Build the parser
parser = yacc.yacc()

# Definir estado / modelo
parser.state = {}
parser.errorLog = []

import sys
files = sys.argv[1:]

for file_name in files:
    try:
        input = open_file(file_name,'YACC')
    except FileNotFoundError:
        input = ""
        print("\033[91m[ERROR] file "+ file_name + " not found.\033[0m")
    if input != "":
        parser.success = True
        parser.parse(input)
        if parser.success:
            lines = input.splitlines()
            file_name = file_name[:-4] 
            print("\033[96m[" + file_name + "]\033[0m\033[92m approved by lexical and syntactic analysis.\033[0m")
            lex_exists, yacc_exists, lines_for_LEX, lines_for_YACC = get_lex_yacc(lines)
            if lex_exists:
                try:                                                               # controlling lex possible errors
                    res = translate_lex(lines_for_LEX)
                    write_file_lex(file_name, res)    
                except VariableError:
                    print("\033[91m[ERROR] variables missing or not introduced with caracter '%' on LEX.\033[0m")
            else:
                print("\033[93m[WARNING] nothing defined for LEX in PLY-Simple.\033[0m")
            if yacc_exists:
                try:                                                           # controlling yacc possible errors
                    res = translate_yacc(lines_for_YACC)
                    write_file_yacc(file_name, res)
                except GrammarError:
                    print("\033[91m[ERROR] grammar not found on YACC.\033[0m")
                except VariableError:
                    print("\033[91m[ERROR] variables missing or not introduced with caracter '%' on YACC.\033[0m")
            else:
                print("\033[93m[WARNING] nothing defined for YACC in PLY-Simple.\033[0m")
        else:
            print("\033[91m[ERROR] file "+ file_name + " does not respect lexical/syntatic structure for PLY-Simple.\033[0m")
            print(parser.errorLog)
            parser.errorLog = []

# python3.9 plySimple_yacc.py example1.txt example2.txt example3.txt example4.txt example5.txt example6.txt example7.txt example8.txt example9.txt example10.txt example11.txt