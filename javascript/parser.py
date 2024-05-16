import ply.yacc as yacc
from lexico import tokens, lexer
from semantic import analyze

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# Diccionario de nombres (para almacenar variables)
names = {}

# Reglas de gramática
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : var_declaration
                 | function_declaration
                 | expression_statement
                 | return_statement'''
    p[0] = p[1]

def p_var_declaration(p):
    '''var_declaration : VAR ID ASSIGN expression SEMICOLON'''
    p[0] = ('var_declaration', p[2], p[4])

def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN parameters RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('function_declaration', p[2], p[4], p[7])

def p_parameters(p):
    '''parameters : ID
                  | parameters COMMA ID
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    p[0] = []

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return_statement', p[2])

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = ('expression_statement', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = ('number', p[1])

def p_expression_id(p):
    '''expression : ID'''
    p[0] = ('id', p[1])

# Regla para manejar errores
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
        parser.errok()
    else:
        print("Syntax error at EOF")

# Construye el parser
parser = yacc.yacc()

def test_lexer(input_string):
    print("Test lexer")
    lexer.input(input_string)
    for tok in lexer:
        print(f"type={tok.type}, value={tok.value}, lineno={tok.lineno}, pos={tok.lexpos}")

def test_parser(input_string):
    result = parser.parse(input_string)
    return result

def print_ast(node, level=0):
    """ Construye y retorna una representación en cadena del AST con sangría para mostrar la estructura. """
    indent = "  " * level  # Crea una cadena de espacios para la sangría
    result = ""

    if isinstance(node, dict):
        # Si el nodo es un diccionario (nodo no terminal)
        node_type = node.get('type', 'Unknown')
        node_info = node.get('info', 'None')
        result += f"{indent}{node_type} (Info: {node_info})\n"
        children = node.get('children', [])
        for child in children:
            result += print_ast(child, level + 1)  # Construye la representación de los hijos recursivamente
    elif isinstance(node, list):
        # Si el nodo es una lista de nodos
        for child in node:
            result += print_ast(child, level)  # Construye la representación de cada nodo de la lista recursivamente
    else:
        # Si es un nodo hoja (valor simple)
        result += f"{indent}- {node}\n"  # Agrega el valor con sangría
    print(result)
    return result

if __name__ == "__main__":
    # Prueba del lexer
    test_input = '''
    var x = 3 + 5;
    function foo(y) {
        return y * 2;
    }
    '''
    print("--------------Prueba del Lexer--------------")
    test_lexer(test_input)
    print("\n--------------Árbol de Análisis Sintáctico--------------")
    result = test_parser(test_input)
    ast = print_ast(result)
    if result:
        semantic = analyze(result, names)
        print("\n--------------Análisis Semántico--------------")
        print(names)
    else:
        print("Error en el análisis sintáctico, no se puede proceder al análisis semántico.")
