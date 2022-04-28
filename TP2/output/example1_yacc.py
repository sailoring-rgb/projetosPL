import ply.yacc as yacc
from example1_lex import *

ts = {}

def p_stat_p1:
    "stat : VAR '=' exp"
    ts[t[1]] = t[3]

def p_stat_p2:
    "stat : exp"
    print(t[1])

def p_exp_p3:
    "exp : exp '+' exp"
    t[0] = t[1] + t[3]

def p_exp_p4:
    "exp : exp '-' exp"
    t[0] = t[1] - t[3]

def p_exp_p5:
    "exp : exp '*' exp"
    t[0] = t[1] * t[3]

def p_exp_p6:
    "exp : exp '/' exp"
    t[0] = t[1] / t[3]

def p_exp_p7:
    "exp : '-' exp"
    t[0] = -t[2]

def p_exp_p8:
    "exp : '(' exp ')'"
    t[0] = t[2]

def p_exp_p9:
    "exp : NUMBER"
    t[0] = t[1]

def p_exp_p10:
    "exp : VAR"
    t[0] = getval(t[1])

def p_error(t):
    print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")

def getval(n):
    if n not in ts: print(f"Undefined name '{n}'")
    return ts.get(n,0)

y = yacc.yacc()
y.parse("3+4*7")