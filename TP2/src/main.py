from lib2to3.pgen2.grammar import Grammar
import sys
from helper import *
from processLEX import *
from processYACC import *

#input_name = input("[PLY-Simple] insert file name (extension included): ")
#input_name = sys.argv[1]
files = sys.argv[1:]

for input_name in files:
    try:
        lines = open_file(input_name)
    except FileNotFoundError:
        lines = ''
        print("\033[91m[ERROR] file "+ input_name + " not found.\033[0m")

    if lines != '':

        lex_exists, yacc_exists, lines_for_LEX, lines_for_YACC = get_lex_yacc(lines)

        if lex_exists:
            try:                                                               # controlling lex possible errors
                res = translate_lex(lines_for_LEX)
                write_file_lex(input_name, res)
                
            except VariableError:
                print("\033[91m[ERROR] variables missing or not introduced with caracter '%' on LEX.\033[0m")
        else:
            print("\033[93m[WARNING] nothing defined for LEX in PLY-Simple.\033[0m")

        if yacc_exists:
            try:                                                           # controlling yacc possible errors
                res = translate_yacc(lines_for_YACC)
                write_file_yacc(input_name, res)
                
            except GrammarError:
                print("\033[91m[ERROR] grammar not found on YACC.\033[0m")

            except VariableError:
                print("\033[91m[ERROR] variables missing or not introduced with caracter '%' on YACC.\033[0m")
        else:
            print("\033[93m[WARNING] nothing defined for YACC in PLY-Simple.\033[0m")