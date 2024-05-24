import ply.yacc as yacc
import re
from math import *
from .node import Node
from .lexico import tokens, lexer

# PARSING
def p_query(t):
    '''query : select 
             | LP query RP
    '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = t[2]

def p_select(t):
    '''select : SELECT list FROM table WHERE lst ORDER BY list
              | SELECT list FROM table WHERE lst
              | SELECT list FROM table ORDER BY list
              | SELECT list FROM table
    '''
    if len(t) == 10:
        t[0] =  Node('QUERY')
        t[0].add( Node('[SELECT]'))
        t[0].add(t[2])
        t[0].add( Node('[FROM]'))
        t[0].add(t[4])
        t[0].add( Node('[WHERE]'))
        t[0].add(t[6])
        t[0].add( Node('[ORDER BY]'))
        t[0].add(t[9])
    elif len(t) == 8:
        t[0] =  Node('QUERY')
        t[0].add( Node('[SELECT]'))
        t[0].add(t[2])
        t[0].add( Node('[FROM]'))
        t[0].add(t[4])
        t[0].add( Node('[ORDER BY]'))
        t[0].add(t[7])
    elif len(t) == 7:
        t[0] =  Node('QUERY')
        t[0].add( Node('[SELECT]'))
        t[0].add(t[2])
        t[0].add( Node('[FROM]'))
        t[0].add(t[4])
        t[0].add( Node('[WHERE]'))
        t[0].add(t[6])
    else:
        t[0] =  Node('QUERY')
        t[0].add( Node('[SELECT]'))
        t[0].add(t[2])
        t[0].add( Node('[FROM]'))
        t[0].add(t[4])

def p_table(t):
    '''table : NAME
             | LP query RP
             | NAME AS NAME
             | table AS NAME
             | table COMMA table
    '''
    if len(t) == 2:
        t[0] =  Node('[TABLE]')
        t[0].add( Node(t[1]))
    elif t[2] == 'AS' and isinstance(t[1],  Node):
        t[0] =  Node('[TABLE]')
        t[0].add(t[1])
        t[0].add( Node('AS'))
        t[0].add( Node(t[3]))
    elif t[2] == 'AS' and not isinstance(t[1],  Node):
        t[0] =  Node('[TABLE]')
        t[0].add( Node(t[1]))
        t[0].add( Node('AS'))
        t[0].add( Node(t[3]))
    elif t[2] == ',':
        t[0] =  Node('[TABLES]')
        t[0].add(t[1])
        t[0].add(t[3])
    else:
        t[0] =  Node('[TABLE]')
        t[0].add(t[2])

def p_lst(t):
    '''lst : condition
           | condition AND condition
           | condition OR condition
           | NAME BETWEEN NUMBER AND NUMBER
           | NAME IN LP query RP
           | NAME '<' agg
           | NAME '>' agg
           | agg '>' NUMBER
           | NAME '=' agg
           | agg '=' NUMBER
           | agg '<' NUMBER
    '''
    if len(t) == 2:
        t[0] =  Node('[CONDITION]')
        t[0].add(t[1])
    elif t[2] == ',':
        t[0] =  Node('[CONDITIONS]')
        t[0].add(t[1])
        t[0].add(t[3])
    elif t[2] == 'AND':
        t[0] =  Node('[CONDITIONS]')
        t[0].add(t[1])
        t[0].add( Node('[AND]'))
        t[0].add(t[3])
    elif t[2] == 'OR':
        t[0] =  Node('[CONDITIONS]')
        t[0].add(t[1])
        t[0].add( Node('[OR]'))
        t[0].add(t[3])
    elif t[2] == 'BETWEEN':
        temp = '%s >= %s & %s <= %s' % (t[1], str(t[3]), t[1], str(t[5]))
        t[0] =  Node('[CONDITION]')
        t[0].add( Node('[TERM]'))
        t[0].add( Node(temp))
    elif t[2] == 'IN':
        t[0] =  Node('[CONDITION]')
        t[0].add( Node(t[1]))
        t[0].add( Node('[IN]'))
        t[0].add(t[4])
    elif t[2] == '<' and len(t) == 4:
        temp = '%s < %s' % (str(t[1]), str(t[3]))
        t[0] =  Node('[CONDITION]')
        t[0].add( Node('[TERM]'))
        t[0].add( Node(temp))
    elif t[2] == '=' and len(t) == 4:
        temp = '%s = %s' % (str(t[1]), str(t[3]))
        t[0] =  Node('[CONDITION]')
        t[0].add( Node('[TERM]'))
        t[0].add( Node(temp))
    elif t[2] == '>' and len(t) == 4:
        temp = '%s > %s' % (str(t[1]), str(t[3]))
        t[0] =  Node('[CONDITION]')
        t[0].add( Node('[TERM]'))
        t[0].add( Node(temp))
    else:
        t[0] =  Node('')

def p_condition(t):
    '''condition : NAME '>' NUMBER
                 | NAME '>' agg  
                 | NAME '<' NUMBER
                 | NAME '<' agg
                 | NAME '=' NUMBER
                 | NAME '=' agg
                 | NAME '>' NAME
                 | NAME '<' NAME
                 | NAME '=' NAME
                 | list '>' list
                 | list '<' list
                 | list '=' list
                 | list '>' NUMBER
                 | list '<' NUMBER
                 | list '=' NUMBER
    '''
    t[0] =  Node('[TERM]')
    if isinstance(t[1],  Node):
        t[0].add(t[1])
    else:
        t[0].add( Node(str(t[1])))
    t[0].add( Node(t[2]))
    if isinstance(t[3],  Node):
        t[0].add(t[3])
    else:
        t[0].add( Node(str(t[3])))

def p_agg(t):
    '''agg : SUM LP NAME RP
           | AVG LP NAME RP
           | COUNT LP NAME RP
           | MIN LP NAME RP 
           | MAX LP NAME RP
           | COUNT LP '*' RP
    '''
    t[0] = '%s(%s)' % (t[1], t[3])

def p_list(t):
    '''list : '*'
            | NAME
            | NAME DOT NAME 
            | list COMMA list
            | list AND NAME
            | list OR NAME        
            | agg
    '''
    if len(t) == 2:
        t[0] =  Node('[FIELD]')
        t[0].add( Node(t[1]))
    elif t[2] == ',':
        t[0] =  Node('[FIELDS]')
        t[0].add(t[1])
        t[0].add(t[3])
    else:
        temp = '%s.%s' % (t[1], t[3])
        t[0] =  Node('[FIELD]')
        t[0].add( Node(temp))

def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()

def test_lexer(input_string):
    """ Ejecuta el lexer sobre el string de entrada y recopila los tokens generados. """
    lexer.input(input_string)
    tokens = []
    for tok in lexer:
        tokens.append(f"type={tok.type}, value={tok.value}")
    return tokens

def test_parser(input_string):
    """ Ejecuta el parser sobre los datos y retorna el resultado del análisis sintáctico. """
    return parser.parse(input_string, lexer=lexer)

def print_ast(node):
    """Construye una representación en cadena del AST con sangría para mostrar la estructura."""
    if not node:
        return "No valid AST generated or parser error."
    
    # Llama a print_node que ahora devuelve una cadena
    return node.print_node(0)

def run_tests(input_string):
    """ Ejecuta todas las pruebas: lexing, parsing y la impresión del AST, y retorna los resultados concatenados en un solo string. """
    # Realiza el análisis léxico
    lexer_results = test_lexer(input_string)
    # Realiza el análisis sintáctico
    parser_results = test_parser(input_string)
    # Genera la representación AST si el parsing fue exitoso
    if parser_results:
        ast_representation = print_ast(parser_results)
    else:
        ast_representation = "No valid AST generated or parser error."

    # Concatena los resultados en un solo string
    final_results = f"Lexer Output:\n{lexer_results}\n\nAST Representation:\n{ast_representation}"
    return final_results
