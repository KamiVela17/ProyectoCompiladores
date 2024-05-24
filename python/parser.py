import ply.yacc as yacc
from .lexico import tokens, lexer
from .semantic import *
# Funciones de parsing que construyen el árbol semántico

# Modificación en p_program
def p_program(p):
    'program : statements'
    p[0] = p[1]

# Modificación en p_statements
def p_statements(p):
    '''
    statements : statement
               | statement statements
    '''
    if len(p) == 2:
        p[0] = ('statements', [p[1]])  
    else:
        p[0] = ('statements', [p[1]] + p[2])

def p_statement(p):
    '''
    statement : function_definition
              | assignment_statement
              | expression_statement
              | return_statement
    '''
    p[0] = p[1]

def p_function_definition(p):
    'function_definition : DEF IDENTIFIER LPAREN opt_parameter_list RPAREN COLON block'
    check_function_defined(p[2])
    add_function_to_context(p[2], p[4])
    p[0] = ('function_definition', p[2], p[4], p[7])
    
def p_return_statement(p):
    'return_statement : RETURN expression SEMICOLON'
    p[0] = ('return_statement', p[2])

# Modificación en p_block
def p_block(p):
    '''
    block : LBRACE statements RBRACE
          | statement
    '''
    if len(p) == 4:
        p[0] = ('block', p[2])
    else:
        p[0] = ('block', [p[1]])


def p_opt_parameter_list(p):
    '''
    opt_parameter_list : parameter_list
                       | empty
    '''
    p[0] = p[1]

def p_parameter_list(p):
    '''
    parameter_list : IDENTIFIER
                   | IDENTIFIER COMMA parameter_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_assignment_statement(p):
    'assignment_statement : IDENTIFIER EQUALS expression SEMICOLON'
    check_assignment_to_function(p[1])
    add_variable_to_context(p[1], p[3])
    p[0] = ('assignment_statement', p[1], p[3])

def p_expression_statement(p):
    'expression_statement : expression SEMICOLON'
    p[0] = ('expression_statement', p[1])

def p_expression(p):
    '''
    expression : term
               | expression PLUS term
               | expression MINUS term
               | IDENTIFIER LPAREN opt_argument_list RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ('operation', p[2], p[1], p[3])
    elif len(p) == 5:  # Para la llamada a función
        check_function_exists(p[1])
        p[0] = ('function_call', p[1], p[3])

# Dentro del archivo parser.py

# Lista de argumentos (opcional): puede haber cero o más argumentos
def p_opt_argument_list(p):
    '''
    opt_argument_list : argument_list
                      | empty
    '''
    p[0] = p[1]

# Lista de argumentos: expresiones separadas por comas
def p_argument_list(p):
    '''
    argument_list : expression
                  | expression COMMA argument_list
    '''
    if len(p) == 2:  # Un solo argumento
        p[0] = [p[1]]
    else:  # Múltiples argumentos
        p[0] = [p[1]] + p[3]

    

def p_term(p):
    '''
    term : factor
         | term TIMES factor
         | term DIVIDE factor
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('operation', p[2], p[1], p[3])

# ... (otras reglas)

# Eliminamos la definición de NEWLINE del lexer

# Agregamos FLOAT y STRING a p_factor
def p_factor(p):
    '''
    factor : NUMBER
           | float_literal
           | string_literal
           | IDENTIFIER
           | LPAREN expression RPAREN
    '''
    if len(p) == 2:
        if p.slice[1].type == 'NUMBER':
            p[0] = ('number', int(p[1]))
        elif p.slice[1].type == 'FLOAT':  # Manejo de FLOAT
            p[0] = ('float', float(p[1]))
        elif p.slice[1].type == 'STRING':  # Manejo de STRING
            p[0] = ('string', p[1][1:-1])  # Quitamos las comillas
        else:
            p[0] = p[1]  
    else:
        p[0] = p[2]
          
# Para FLOAT
def p_float_literal(p):
    'float_literal : FLOAT'
    p[0] = ('float_literal', float(p[1]))  # Convierte el token a un número flotante

# Para NEWLINE (se puede ignorar)
def p_newline(p):
    'newline : NEWLINE'
    p[0] = None  # No hacer nada con los saltos de línea

# Para STRING
def p_string_literal(p):
    'string_literal : STRING'
    p[0] = ('string_literal', p[1][1:-1])  # Quita las comillas del string


def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value '{p.value}' at line {p.lineno}")
    else:
        print("Syntax error at EOF")
        
import ply.lex as lex
import ply.yacc as yacc

# Suponemos que lexer y parser están definidos y configurados aquí

parser = yacc.yacc()

def test_lexer(input_string):
    """ Ejecuta el lexer sobre el string de entrada y recopila los tokens generados. """
    lexer.input(input_string)
    tokens = []
    for tok in lexer:
        token_info = f"type={tok.type}, value={tok.value}, lineno={tok.lineno}, pos={tok.lexpos}"
        tokens.append(token_info)
    return '\n'.join(tokens)

def test_parser(input_string):
    """ Ejecuta el parser sobre el string de entrada y retorna el resultado del análisis sintáctico. """
    result = parser.parse(input_string, lexer=lexer)
    return result

def print_ast(node, level=0):
    """ Construye una representación en cadena del AST con sangría para mostrar la estructura. """
    result = ""
    indent = "  " * level
    
    if isinstance(node, tuple):
        result += f"{indent}{node[0]}\n"  # Agrega el tipo de nodo
        for child in node[1:]:
            result += print_ast(child, level + 1)
    elif isinstance(node, list):
        for child in node:
            result += print_ast(child, level)
    else:
        result += f"{indent}- {node}\n"
    return result

def run_tests(input_string):
    """ Ejecuta las pruebas del lexer, parser y muestra el AST, consolidando todo en un único string de salida. """
    results = []
    results.append("-------------- Testing Lexer --------------\n")
    lexer_results = test_lexer(input_string)
    results.append(lexer_results)

    results.append("\n-------------- Testing Parser --------------\n")
    parser_result = test_parser(input_string)
    if parser_result:
        results.append("\n-------------- AST Representation --------------\n")
        ast_representation = print_ast(parser_result)
        results.append(ast_representation)
    else:
        results.append("No valid AST generated or parser error.\n")

    return '\n'.join(results)