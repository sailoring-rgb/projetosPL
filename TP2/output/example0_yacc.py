import ply.yacc as yacc
from example0_lex import *

# GRAMMAR:
# p1:    Lista -> PA PF
# p2:      | PA Elems PF
# p3:    Elems -> Elem Resto
# p4:    Resto -> 
# p5:      | VIRG Elems
# p6:    Elem -> NUM
# p7:      | Lista



def p_Lista_p1(p):
    "Lista : PA PF"
    

def p_Lista_p2(p):
    "Lista : PA Elems PF"
    

def p_Elems_p3(p):
    "Elems : Elem Resto"
    

def p_Resto_p4(p):
    "Resto : "
    

def p_Resto_p5(p):
    "Resto : VIRG Elems"
    

def p_Elem_p6(p):
    "Elem : NUM"
    

def p_Elem_p7(p):
    "Elem : Lista"
    

def p_error(p):
    print("Erro sintático",p)

parser = yacc.yacc()
