import ply.lex as lex

# TOKENS
tokens = (
    'SELECT', 'FROM', 'WHERE', 'ORDER', 'BY', 'NAME', 'AND', 'OR', 'COMMA',
    'LP', 'RP', 'AVG', 'BETWEEN', 'IN', 'SUM', 'MAX', 'MIN', 'COUNT', 'NUMBER', 'AS', 'DOT'
)

literals = ['=', '+', '-', '*', '^', '>', '<']

# DEFINE OF TOKENS
def t_LP(t):
    r'\('
    return t

def t_DOT(t):
    r'\.'
    return t

def t_AS(t):
    r'AS'
    return t

def t_SUM(t):
    r'SUM'
    return t

def t_MIN(t):
    r'MIN'
    return t

def t_MAX(t):
    r'MAX'
    return t

def t_COUNT(t):
    r'COUNT'
    return t

def t_AVG(t):
    r'AVG'
    return t

def t_RP(t):
    r'\)'
    return t

def t_BETWEEN(t):
    r'BETWEEN'
    return t

def t_IN(t):
    r'IN'
    return t

def t_SELECT(t):
    r'SELECT'
    return t

def t_FROM(t):
    r'FROM'
    return t

def t_WHERE(t):
    r'WHERE'
    return t

def t_ORDER(t):
    r'ORDER'
    return t

def t_BY(t):
    r'BY'
    return t

def t_OR(t):
    r'OR'
    return t

def t_AND(t):
    r'AND'
    return t

def t_COMMA(t):
    r','
    return t

def t_NUMBER(t):
    r'[0-9]+'
    return t

def t_NAME(t):
    r'[A-Za-z]+|[a-zA-Z_][a-zA-Z0-9_]*|[A-Z]*\.[A-Z]$'
    return t

# IGNORED
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()