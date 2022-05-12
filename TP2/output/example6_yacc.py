import ply.yacc as yacc
from example6_lex import *

# GRAMMAR:
# p1:    Lista -> Lista
# p2:      | Lista Ficheiro
# p3:      | 
# p4:    Ficheiro -> '(' id id ')'



def p_Lista_p1(p):
    "Lista : Lista"
    
def p_Lista_p2(p):
    "Lista : Lista Ficheiro"
    
def p_Lista_p3(p):
    "Lista : "
    
def p_Ficheiro_p4(p):
    "Ficheiro : '(' id id ')'"
    p.parser.itens.appen(p[2])
def p_error(p):
    print("Erro sintático: ", p)
    parser.success = False

parser = yacc.yacc()
parser.itens = []    
