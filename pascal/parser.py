import ply.yacc as yacc
from .lexico import tokens, lexer

TEST_ERROR = 1

# PRECEDENCE
precedence = (
    # Relational Operators ( = )
    ('right', 'EQ'),
    # Relational Operators ( := )
    ('right', 'EQUALS'),
    # Relational Operators ( <> )
    ('left', 'NEQ'),
    # Relational Operators ( <  <=  > )
    ('left', 'LT', 'LE', 'GT', 'GE'),
    # Arithmetic Operators ( +  - )
    ('left', 'PLUS', 'MINUS'),
    # Arithmetic Operators ( *  / )
    ('left', 'TIMES', 'DIVIDE'),
    # Delimeters ( (  ) )
    ('left', 'LPAREN', 'RPAREN'),
)

# GRAMMAR RULES
# PROGRAM
def p_program(p):
    'program : PROGRAM ID SEMICOLON block POINT'
    p[0] = ('program', p[2], p[4])

# BLOCK
def p_block(p):
    'block : labelDecl constDecl varDecl BEGIN procDecl functDecl statement END'
    p[0] = ('block', p[1], p[2], p[3], p[5], p[6], p[7])

# LABEL
def p_labelDecl(p):
    'labelDecl : LABEL NUMBER SEMICOLON'
    p[0] = ('labelDecl', p[2])

def p_labelDeclEmpty(p):
    'labelDecl : empty'
    p[0] = None

# CONST
def p_constDeclEmpty(p):
    'constDecl : empty'
    p[0] = None

def p_constDecl(p):
    'constDecl : CONST constAssignmentList SEMICOLON'
    p[0] = ('constDecl', p[2])

def p_constAssignmentList_1(p):
    'constAssignmentList : ID EQ INTEGER'
    p[0] = [('constAssignment', p[1], p[3])]

def p_constAssignmentList_2(p):
    'constAssignmentList : ID EQ REAL'
    p[0] = [('constAssignment', p[1], p[3])]

def p_constAssignmentList_3(p):
    'constAssignmentList : ID EQ STRING'
    p[0] = [('constAssignment', p[1], p[3])]

def p_constAssignmentList_4(p):
    'constAssignmentList : ID EQ NUMBER'
    p[0] = [('constAssignment', p[1], p[3])]

def p_constAssignmentList_5(p):
    'constAssignmentList : ID EQ BOOLEAN'
    p[0] = [('constAssignment', p[1], p[3])]

# TYPE
def p_typeDefinitionEmpty(p):
    'typeDefinition : empty'
    p[0] = None

def p_typeDefinition_1(p):
    'typeDefinition : INTEGER'
    p[0] = 'integer'

def p_typeDefinition_2(p):
    'typeDefinition : REAL'
    p[0] = 'real'

def p_typeDefinition_3(p):
    'typeDefinition : STRING'
    p[0] = 'string'

def p_typeDefinition_4(p):
    'typeDefinition : BOOLEAN'
    p[0] = 'boolean'

# VAR
def p_varDeclEmpty(p):
    'varDecl : empty'
    p[0] = None

def p_varDecl(p):
    'varDecl : VAR identList COLON typeDefinition SEMICOLON identList_2'
    p[0] = ('varDecl', p[2], p[4], p[6])

def p_identList_1(p):
    'identList : ID'
    p[0] = [p[1]]

def p_identList_2(p):
    'identList : identList COMMA ID'
    p[0] = p[1] + [p[3]]

def p_identList_3(p):
    'identList_2 : empty'
    p[0] = None

def p_identList_4(p):
    'identList_2 : identList COLON typeDefinition SEMICOLON identList_2'
    p[0] = (p[1], p[3], p[5])

# PROCEDURE
def p_procDecl1(p):
    'procDecl : PROCEDURE ID LPAREN parameters RPAREN SEMICOLON block SEMICOLON'
    p[0] = ('procDecl', p[2], p[4], p[7])

def p_procDeclEmpty(p):
    'procDecl : empty'
    p[0] = None

# FUNCTION
def p_functDeclEmpty(p):
    'functDecl : empty'
    p[0] = None

def p_functDecl1(p):
    'functDecl : FUNCTION ID LPAREN parameters RPAREN COLON typeDefinition SEMICOLON block SEMICOLON'
    p[0] = ('functDecl', p[2], p[4], p[7], p[9])

# PARAMETERS
def p_parametersEmpty(p):
    'parameterList : empty'
    p[0] = None

def p_parameters(p):
    'parameters : parameterList'
    p[0] = p[1]

def p_parameterList_1(p):
    'parameterList : parameterList SEMICOLON parameter'
    p[0] = p[1] + [p[3]]

def p_parameterList_2(p):
    'parameterList : parameter'
    p[0] = [p[1]]

def p_parameter_1(p):
    'parameter : ID COLON typeDefinition'
    p[0] = (p[1], p[3])

def p_parameter_2(p):
    'parameter : ID COMMA parameter'
    p[0] = (p[1], p[3])

def p_parameter_3(p):
    'parameter : COLON typeDefinition'
    p[0] = p[2]

# STATEMENT
def p_statementEmpty(p):
    'statement : empty'
    p[0] = None

def p_statement_1(p):
    'statement : statement ID EQUALS expression SEMICOLON'
    p[0] = ('assignment', p[2], p[4])

def p_statement_2(p):
    'statement : BEGIN statementList END'
    p[0] = ('begin', p[2])

def p_statement_3(p):
    'statement : statement IF condition THEN statement'
    p[0] = ('if', p[3], p[5])

def p_statement_4(p):
    'statement : statement IF condition THEN statement ELSE statement'
    p[0] = ('if', p[3], p[5], p[7])

def p_statement_5(p):
    'statement : WHILE condition DO statement'
    p[0] = ('while', p[2], p[4])

# STATEMENT - List
def p_statementList_1(p):
    'statementList : statement'
    p[0] = [p[1]]

def p_statementList_2(p):
    'statementList : statementList SEMICOLON statement'
    p[0] = p[1] + [p[3]]

# STATEMENT - condition
def p_condition(p):
    'condition : expression relation expression'
    p[0] = (p[2], p[1], p[3])

# STATEMENT - relation
def p_relation_1(p):
    'relation : EQUALS'
    p[0] = 'equals'

def p_relation_2(p):
    'relation : LT'
    p[0] = 'lt'

def p_relation_3(p):
    'relation : LE'
    p[0] = 'le'

def p_relation_4(p):
    'relation : GT'
    p[0] = 'gt'

def p_relation_5(p):
    'relation : GE'
    p[0] = 'ge'

def p_relation_6(p):
    'relation : EQ'
    p[0] = 'eq'

def p_relation_7(p):
    'relation : NEQ'
    p[0] = 'neq'

# STATEMENT - expression
def p_expression_1(p):
    'expression : term'
    p[0] = p[1]

def p_expression_2(p):
    'expression : addOperator term'
    p[0] = (p[1], p[2])

def p_expression_3(p):
    'expression : expression addOperator term'
    p[0] = (p[2], p[1], p[3])

def p_addOperator_1(p):
    'addOperator : PLUS'
    p[0] = '+'

def p_addOperator_2(p):
    'addOperator : MINUS'
    p[0] = '-'

def p_term_1(p):
    'term : factor'
    p[0] = p[1]

def p_term_2(p):
    'term : term multOperator factor'
    p[0] = (p[2], p[1], p[3])

def p_multOperator_1(p):
    'multOperator : TIMES'
    p[0] = '*'

def p_multOperator_2(p):
    'multOperator : DIVIDE'
    p[0] = '/'

def p_factor_1(p):
    'factor : ID'
    p[0] = ('id', p[1])

def p_factor_2(p):
    'factor : REAL'
    p[0] = ('real', p[1])

def p_factor_3(p):
    'factor : INTEGER'
    p[0] = ('integer', p[1])

def p_factor_4(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_5(p):
    'factor : NUMBER'
    p[0] = ('number', p[1])

def p_factor_6(p):
    'factor : BOOLEAN'
    p[0] = ('boolean', p[1])

def p_empty(p):
    'empty :'
    p[0] = None

# ERROS
def p_error(p):
    if TEST_ERROR:
        if p is not None:
            print("Context Error: '%s'" % (str(p.value)))
            print("   -> Sintax Error! Line: '%s'" % (str(p.lexer.lineno)))
        else:
            print("   -> Lexer Error! Line: '%s'" % uLexico.lexer.lineno)
    else:
        raise Exception('Syntax', 'Error')

# Suponemos que lexer y parser están definidos y configurados aquí

parser = yacc.yacc()

def test_lexer(data):
    """ Ejecuta el lexer y retorna la lista de tokens generados a partir del string de entrada como string. """
    lexer.input(data)
    tokens = []
    for tok in lexer:
        tokens.append(f"type={tok.type}, value={tok.value}, lineno={tok.lineno}, pos={tok.lexpos}")
    return '\n'.join(tokens)

def test_parser(data):
    """ Ejecuta el parser sobre los datos y retorna el resultado del análisis sintáctico como string. """
    result = parser.parse(data, lexer=lexer)
    return str(result) if result else "No valid AST generated."

def print_ast(node, level=0):
    """ Construye y retorna una representación en cadena del AST con sangría para mostrar la estructura. """
    indent = "  " * level
    result = ""
    
    if isinstance(node, dict):
        node_type = node.get('type', 'Unknown')
        node_info = node.get('info', 'None')
        result += f"{indent}{node_type} (Info: {node_info})\n"
        children = node.get('children', [])
        for child in children:
            result += print_ast(child, level + 1)
    elif isinstance(node, list):
        for child in node:
            result += print_ast(child, level)
    else:
        result += f"{indent}- {node}\n"
    return result

def run_tests(data):
    """ Ejecuta tests para lexer y parser, e imprime los resultados incluyendo la representación del AST si está disponible. """
    results = []
    results.append("----- Testing Lexer -----\n")
    lexer_results = test_lexer(data)
    results.append(lexer_results)

    results.append("\n----- Testing Parser -----\n")
    parser_result = test_parser(data)
    results.append(parser_result)

    if parser_result != "No valid AST generated.":
        results.append("\n----- AST Representation -----\n")
        ast_representation = print_ast(parser_result)
        results.append(ast_representation)
    else:
        results.append("\nNo valid AST generated.\n")

    return '\n'.join(results)