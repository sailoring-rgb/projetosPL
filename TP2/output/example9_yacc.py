import ply.yacc as yacc
from example9_lex import *

# GRAMMAR:
# p1:    S -> Z S Z
# p2:      | U S U
# p3:      | Z
# p4:      | U



def p_S_p1(p):
    "S : Z S Z"
    

def p_S_p2(p):
    "S : U S U"
    

def p_S_p3(p):
    "S : Z"
    

def p_S_p4(p):
    "S : U"
    

def p_error(p):
    print("Erro sintático: ", p)
    parser.success = False

parser = yacc.yacc()
