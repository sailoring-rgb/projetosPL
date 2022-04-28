from helper import *
from processLEX import *
from processYACC import *

input_name, lines = open_file()
lines_for_LEX, lines_for_YACC = get_lex_yacc(lines)

"""
print("-------------------------------------FOR LEX---------------------------------------------")
for line in lines_for_LEX:
    print(line)
print("-------------------------------------FOR YACC---------------------------------------------")
for line in lines_for_YACC:
    print(line)
"""

res = translate_lex(lines_for_LEX)

write_file_lex(input_name, res)

res = translate_yacc(lines_for_YACC)

write_file_yacc(input_name, res)