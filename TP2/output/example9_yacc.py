import ply.yacc as yacc
from example9_lex import *

# GRAMMAR:
# p1:    Lista -> Lista Ficheiro
# p2:      | 
# p3:    Ficheiro -> '(' id id ')'



def p_Lista_p1(p):
    "Lista : Lista Ficheiro"
    

def p_Lista_p2(p):
    "Lista : "
    

def p_Ficheiro_p3(p):
    "Ficheiro : '(' id id ')'"
    p.parser.itens.appen(p[2])

def p_error(p): 
    print("Erro sintático: ", p)
    parser.success = False

parser = yacc.yacc()
parser.itens = []    
