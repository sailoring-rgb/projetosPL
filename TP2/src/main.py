import sys
from helper import *

files = sys.argv[1:]

for input_name in files:
    try:
        lines = open_file(input_name)
    except FileNotFoundError:
        lines = ''
        print("\033[91m[ERROR] file "+ input_name + " not found.\033[0m")

    if lines != '':

        lex_exists, yacc_exists, lines_for_LEX, lines_for_YACC = get_lex_yacc(lines)

        res = translate_lex(lines_for_LEX)
        write_file_lex(input_name, res)
                
        res = translate_yacc(lines_for_YACC)
        write_file_yacc(input_name, res)