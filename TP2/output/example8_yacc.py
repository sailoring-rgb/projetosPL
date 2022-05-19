import ply.yacc as yacc
from example8_lex import *

# GRAMMAR:
# p1:    ABin -> PA PF
# p2:      | PA NUM ABin ABin PF



def p_ABin_p1(p):
    "ABin : PA PF"
    

def p_ABin_p2(p):
    "ABin : PA NUM ABin ABin PF"
    

def p_error(p): 
    print("Erro sintático: ", p)
    parser.success = False

parser = yacc.yacc()
parser.abins = []   
