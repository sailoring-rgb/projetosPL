import ply.yacc as yacc
from example8_lex import *

# GRAMMAR:
# p1:    Calc -> Comandos FIM
# p2:    Comandos -> Comandos Comando
# p3:      | Comando
# p4:    Comando -> id '=' Exp
# p5:      | '!' Exp
# p6:      | '?' id
# p7:      | DUMP
# p8:    Exp -> Exp '+' Termo
# p9:      | Exp '-' Termo
# p10:      | Termo
# p11:    Termo -> Termo '*' Fator
# p12:      | Fator
# p13:    Fator -> num
# p14:      | '(' Exp ')'
# p15:      | id



def p_Calc_p1(p):
    "Calc : Comandos FIM"
    

def p_Comandos_p2(p):
    "Comandos : Comandos Comando"
    

def p_Comandos_p3(p):
    "Comandos : Comando"
    

def p_Comando_p4(p):
    "Comando : id '=' Exp"
    p.parser.registos[p[1]] = p[3]

def p_Comando_p5(p):
    "Comando : '!' Exp"
    print(p[2])

def p_Comando_p6(p):
    "Comando : '?' id"
    p.parser.registos[p[2]]

def p_Comando_p7(p):
    "Comando : DUMP"
    

def p_Exp_p8(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3]

def p_Exp_p9(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] - p[3]

def p_Exp_p10(p):
    "Exp : Termo"
    p[0] = p[1]

def p_Termo_p11(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] * p[3]

def p_Termo_p12(p):
    "Termo : Fator"
    p[0] = p[1]

def p_Fator_p13(p):
    "Fator : num"
    p[0] = p[1]

def p_Fator_p14(p):
    "Fator : '(' Exp ')'"
    p[0] = p[2]

def p_Fator_p15(p):
    "Fator : id"
    p[0] = p.parser.registos[p[1]]

parser = yacc.yacc()
parser.registos = {} 
