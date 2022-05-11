import ply.yacc as yacc
from example4_lex import *

# GRAMMAR:
# p1:    Z -> Exp FIM
# p2:    Exp -> '(' '+' Lista Exp ')'
# p3:      | '(' '*' Lista Exp ')'
# p4:      | num
# p5:    Lista -> Lista Exp
# p6:      | Exp



def produtorio(lista):
    res = 1
    for elem in lista:
        res *= elem
    return res

def somatorio(lista):
    res = 0
    for elem in lista:
        res += elem
    return res

def p_Z_p1(p):
    "Z : Exp FIM"
    print("Resultado: ", p[1])

def p_Exp_p2(p):
    "Exp : '(' '+' Lista Exp ')'"
    p[0] = somatorio(p[3]) + p[4]

def p_Exp_p3(p):
    "Exp : '(' '*' Lista Exp ')'"
    p[0] = produtorio(p[3]) * p[4]

def p_Exp_p4(p):
    "Exp : num"
    p[0] = p[1]

def p_Lista_p5(p):
    "Lista : Lista Exp"
    p[0] = p[1] + [p[2]]

def p_Lista_p6(p):
    "Lista : Exp"
    p[0] = [p[1]]

def p_error(p):
    print("Erro sintático: ", p)
    parser.success = False


parser = yacc.yacc()
import sys
for linha in sys.stdin:
      parser.success = True
      parser.parse(linha)
      if parser.success:
          print('Frase válida: ', linha)
      else:
          print('Frase inválida.')
