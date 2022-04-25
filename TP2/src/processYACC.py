import re
from typing import List


example = ["stat : VAR '=' exp              { ts[t[1]] = t[3] }", "stat : exp                      { print(t[1]) }", "exp  : exp '+' exp              { t[0] = t[1] + t[3] }",
"exp  : exp '-' exp              { t[0] = t[1] - t[3] }", "exp  : exp '*' exp              { t[0] = t[1] * t[3] }", "exp  : exp '/' exp              { t[0] = t[1] / t[3] }",
"exp  : '-' exp %prec UMINUS     { t[0] = -t[2] }", "exp  : '(' exp ')'              { t[0] = t[2] }", "exp  : NUMBER                   { t[0] = t[1] }", "exp  : VAR                      { t[0] = getval(t[1]) }"]


def process_grammar(grammar: List[str]):

    for line in grammar:
        pass