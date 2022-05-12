import ply.yacc as yacc
from example1_lex import *

# GRAMMAR:
# p1:    stat -> VAR '=' exp
# p2:      | exp
# p3:    exp -> exp '+' exp
# p4:      | exp '-' exp
# p5:      | exp '*' exp
# p6:      | exp '/' exp
# p7:      | '-' exp
# p8:      | '(' exp ')'
# p9:      | NUMBER
# p10:      | VAR

precedence = [
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
]

ts = {}

def getval(n):
    if n not in ts: print(f"Undefined name '{n}'")
    return ts.get(n,0)

def p_stat_p1(p):
    "stat : VAR '=' exp"
    ts[p[1]] = p[3]
def p_stat_p2(p):
    "stat : exp"
    print(p[1])
def p_exp_p3(p):
    "exp : exp '+' exp"
    p[0] = p[1] + p[3]
def p_exp_p4(p):
    "exp : exp '-' exp"
    p[0] = p[1] - p[3]
def p_exp_p5(p):
    "exp : exp '*' exp"
    p[0] = p[1] * p[3]
def p_exp_p6(p):
    "exp : exp '/' exp"
    p[0] = p[1] / p[3]
def p_exp_p7(p):
    "exp : '-' exp"
    p[0] = -p[2]
def p_exp_p8(p):
    "exp : '(' exp ')'"
    p[0] = p[2]
def p_exp_p9(p):
    "exp : NUMBER"
    p[0] = p[1]
def p_exp_p10(p):
    "exp : VAR"
    p[0] = getval(p[1])
def p_error(t):
    print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")

y=yacc()
y.parse("3+4*7")
