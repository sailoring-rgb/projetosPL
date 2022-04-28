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

ex = ["stat : VAR '=' exp              { ts[t[1]] = t[3]}",
"stat : exp                      { print(t[1]) }",
"exp  : exp '+' exp              { t[0] = t[1] + t[3] }",
"exp  : exp '-' exp              { t[0] = t[1] - t[3] }",
"exp  : exp '*' exp              { t[0] = t[1] * t[3] }",
"exp  : exp '/' exp              { t[0] = t[1] / t[3] }",
"exp  : '-' exp %prec UMINUS     { t[0] = -t[2] }",
"exp  : '(' exp ')'              { t[0] = t[2] }",
"exp  : NUMBER                   { t[0] = t[1] }",
"exp  : VAR                      { t[0] = getval(t[1]) }"]
"""

res = translate_lex(lines_for_LEX)

write_file_lex(input_name, res)

res = translate_yacc(lines_for_YACC)

write_file_yacc(input_name, res)