import ply.yacc as yacc
from example1_lex import tokens, literals

## YACC

"""
Gramática:
Stat -> VAR '=' Exp      # p1
      | Exp              # p2

Exp -> Exp '+' Exp       # p3
     | Exp '-' Exp       # p4
     | Exp '*' Exp       # p5
     | Exp '/' Exp       # p6
     | '-' Exp           # p7
     | '(' Exp ')'       # p8
     | NUMBER            # p9
     | VAR               # p10
"""

"""
>>>>>>> MUITO SINCERAMENTE, NÃO SEI O QUE FAZER COM ISTO. PERCEBO, MAS NÃO SEI A UTILIDADE.
precedence = [
                ('left','+','-'),
                ('left','*','/'),
                ('right','UMINUS'),
             ]
"""

# symboltable : dictionary of variables
ts = {}

def p_Stat_p1(t):
    "Stat : VAR '=' Exp"
    ts[p[1]] = t[3]

def p_Stat_p2(t):
    "Stat : Exp"
    print(t[1])

def p_Exp_p3(t):
    "Exp : Exp '+' Exp"
    t[0] = t[1] + t[3]

def p_Exp_p4(t):
    "Exp : Exp '-' Exp"
    t[0] = t[1] - t[3]

def p_Exp_p5(t):
    "Exp : Exp '*' Exp"
    t[0] = t[1] * t[3]

def p_Exp_p6(t):
    "Exp : Exp '/' Exp"
    t[0] = t[1] / t[3]

def p_Exp_p7(t):
    "Exp : '-' Exp"
    t[0] = -t[2]

def p_Exp_p8(t):
    "Exp : '(' Exp ')'"
    t[0] = t[2]

def p_Exp_p9(t):
    "Exp : NUMBER"
    t[0] = t[1]

def p_Exp_p10(t):
    "Exp : VAR"
    t[0] = getval(t[1])


def p_error(t):
    print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")

def getval(n):
    if n not in ts: print(f"Undefined name '{n}'")
    return ts.get(n,0)

y = yacc.yacc()
y.parse("3+4*7")