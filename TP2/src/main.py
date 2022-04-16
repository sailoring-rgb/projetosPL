from helper import *

lines = open_file()
lines_for_LEX, lines_for_YACC = lex_or_yacc(lines)

"""
print("-------------------------------------FOR LEX---------------------------------------------")
for line in lines_for_LEX:
    print(line)
print("-------------------------------------FOR YACC---------------------------------------------")
for line in lines_for_YACC:
    print(line)
"""

translate_lex(lines_for_LEX)