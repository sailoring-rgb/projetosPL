from helper import *
from processLEX import *
from processYACC import *

input_name, lines = open_file()

lines_for_LEX, lines_for_YACC = get_lex_yacc(lines)

try:
    res = translate_lex(lines_for_LEX)
    write_file_lex(input_name, res)

    try:
        res = translate_yacc(lines_for_YACC)
        write_file_yacc(input_name, res)
    except NameError:
        pass

except NameError:
    print('\033[93m' + "ERROR TRANSLATING LEX: variables missing or not introduced with caracter '%'" + '\033[0m')