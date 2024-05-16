import ply.yacc as yacc
from lexico import tokens, lexer
import semantic  # Importamos las funciones de semantic.py

# Funciones de parsing que construyen el árbol semántico

# Modificación en p_program
import ply.yacc as yacc
from lexico import tokens, lexer
import semantic  

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
    semantic.check_function_defined(p[2])
    semantic.add_function_to_context(p[2], p[4])
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
    semantic.check_assignment_to_function(p[1])
    semantic.add_variable_to_context(p[1], p[3])
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
        semantic.check_function_exists(p[1])
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

# Construye el parser
parser = yacc.yacc()

def test_lexer(input_string):
    lexer.input(input_string)
    for tok in lexer:
        print(f"type={tok.type}, value={tok.value}, lineno={tok.lineno}, pos={tok.lexpos}")
        
def test_parser(input_string):
    result = parser.parse(input_string)
    print(result)
    return result


def print_ast(node, level=0):
    """Imprime el AST de forma recursiva con sangría para mostrar la estructura."""

    if isinstance(node, tuple):  
        # Si es un nodo no terminal (una tupla)
        print("  " * level + node[0])  # Imprimir tipo de nodo con sangría
        for child in node[1:]:
            print_ast(child, level + 1)  # Imprimir hijos recursivamente
    elif isinstance(node, list): 
        # Si es una lista de nodos
        for child in node:
            print_ast(child, level)   # Imprimir cada nodo de la lista recursivamente
    else:
        # Si es un nodo hoja (un valor simple)
        print("  " * level + f"- {node}")  # Imprimir valor con sangría

# Test the parser
if __name__ == "__main__":
    test_input = 'def metodo(x, y): return x + y;'
    test_lexer(test_input)
    result = test_parser(test_input)
    print("\n--------------Árbol de Análisis Sintáctico--------------")
    print_ast(result)
