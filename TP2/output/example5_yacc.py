import ply.yacc as yacc
from example5_lex import *

# GRAMMAR:
# p1:    S -> A a S
# p2:      | A
# p3:    A -> A a F
# p4:      | F
# p5:    F -> F S



def p_S_p1(p):
    "S : A a S"
    

def p_S_p2(p):
    "S : A"
    

def p_A_p3(p):
    "A : A a F"
    

def p_A_p4(p):
    "A : F"
    

def p_F_p5(p):
    "F : F S"
    

def p_error(p): 
    print("Erro sintático: ", p)
    parser.success = False

parser = yacc.yacc()
