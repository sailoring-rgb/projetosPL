# Production rules
def p_plySimple_EOF(p):
    "Ply-Simple : EOF"

def p_plySimple_BLEX(p):
    "Ply-Simple : BLEX Lex BYACC Yacc EOF"

def p_plySimple_BYACC(p):
    "Ply-Simple : BYACC Yacc BLEX Lex EOF"

def p_Calc(p):
    'Calc : Comandos FIM'

def p_Lex(p):
    'Lex : Vars Funs'

def p_Vars(p):
    'Vars : Var RestVars'

def p_Var_Literals(p):
    "Var : LIT literals"

def p_Var_Ignore(p):
    "Var : IGN ignore"

def p_Var_ListTok(p):
    "Var : TOK ListTok"

def p_RestVars_NLINE(p):
    "RestVars : NLINE Vars"

def p_RestVars_Empty(p):
    "RestVars : "

def p_ListTok(p):
    "ListTok : token ResTok"

def p_RestTok_VIRG(p):
    "RestTok : VIRG ListTok"

def p_RestTok_Empty(p):
    "RestTok : "

def p_Funs(p):
    "Funs : Fun RestFun"

def p_Fun(p):
    "Fun : regex FunOP"

def p_FunOP_Result(p):
    "FunOP : RET result"

def p_FunOP_Erro(p):
    "FunOP : ERR erro"

def p_RestFun_SEP(p):
    "RestFun : SEP Funs"

def p_RestFun_Empty(p):
    "RestFun : "

def p_Yacc(p):
    "Yacc : PrecList ListProd"

def p_PrecList(p):
    "PrecList : Predence PrecRest"

def p_Predence(p):
    "Predence : PREC cenas"

def p_PrecREst_SEP2(p):
    "PrecRest : SEP2 PrecList"

def p_PrecREst_Empty(p):
    "PrecRest : "

def p_ListProd(p):
    "ListProd : Prod RestProd"

def p_Prod(p):
    "Prod : regra TAB prodOp"

def p_RestProd_SEP3(p):
    "RestProd : SEP3 ListProd"
    
def p_RestProd_Empty(p):
    "RestProd : "