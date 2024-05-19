import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens
tokens = (
    'AND', 'ARRAY', 'BEGIN', 'BOOLEAN', 'CASE', 'CHAR', 'CHR', 'CONST', 'DIV', 'DO', 'DOWNTO',
    'ELSE', 'END', 'FILE', 'FOR', 'FUNCTION', 'GOTO', 'IF', 'IN', 'INTEGER', 'LABEL', 'MOD', 'NIL', 'NOT', 'OF', 'OR',
    'PACKED', 'PROCEDURE', 'PROGRAM', 'REAL', 'RECORD', 'REPEAT', 'SET', 'THEN', 'TO', 'TYPE', 'UNTIL', 'VAR', 'WHILE',
    'WITH', 'PLUS', 'MINUS', 'STAR', 'SLASH', 'ASSIGN', 'COMMA', 'SEMI', 'COLON', 'EQUAL', 'NOT_EQUAL', 'LT', 'LE',
    'GE', 'GT', 'LPAREN', 'RPAREN', 'LBRACK', 'LBRACK2', 'RBRACK', 'RBRACK2', 'POINTER', 'AT', 'DOT', 'DOTDOT',
    'LCURLY', 'RCURLY', 'UNIT', 'INTERFACE', 'USES', 'STRING', 'IMPLEMENTATION', 'TRUE', 'FALSE', 'IDENT', 'STRING_LITERAL',
    'NUM_INT', 'NUM_REAL'
)

# Reglas de expresión regular para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_ASSIGN = r':='
t_COMMA = r','
t_SEMI = r';'
t_COLON = r':'
t_EQUAL = r'='
t_NOT_EQUAL = r'<>'
t_LT = r'<'
t_LE = r'<='
t_GE = r'>='
t_GT = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_LBRACK2 = r'\(\.'
t_RBRACK = r'\]'
t_RBRACK2 = r'\.\)'
t_POINTER = r'\^'
t_AT = r'@'
t_DOT = r'\.'
t_DOTDOT = r'\.\.'
t_LCURLY = r'\{'
t_RCURLY = r'\}'

# Definición de tokens para palabras reservadas
reserved = {
    'AND': 'AND',
    'ARRAY': 'ARRAY',
    'BEGIN': 'BEGIN',
    'BOOLEAN': 'BOOLEAN',
    'CASE': 'CASE',
    'CHAR': 'CHAR',
    'CHR': 'CHR',
    'CONST': 'CONST',
    'DIV': 'DIV',
    'DO': 'DO',
    'DOWNTO': 'DOWNTO',
    'ELSE': 'ELSE',
    'END': 'END',
    'FILE': 'FILE',
    'FOR': 'FOR',
    'FUNCTION': 'FUNCTION',
    'GOTO': 'GOTO',
    'IF': 'IF',
    'IN': 'IN',
    'INTEGER': 'INTEGER',
    'LABEL': 'LABEL',
    'MOD': 'MOD',
    'NIL': 'NIL',
    'NOT': 'NOT',
    'OF': 'OF',
    'OR': 'OR',
    'PACKED': 'PACKED',
    'PROCEDURE': 'PROCEDURE',
    'PROGRAM': 'PROGRAM',
    'REAL': 'REAL',
    'RECORD': 'RECORD',
    'REPEAT': 'REPEAT',
    'SET': 'SET',
    'THEN': 'THEN',
    'TO': 'TO',
    'TYPE': 'TYPE',
    'UNTIL': 'UNTIL',
    'VAR': 'VAR',
    'WHILE': 'WHILE',
    'WITH': 'WITH',
    'UNIT': 'UNIT',
    'INTERFACE': 'INTERFACE',
    'USES': 'USES',
    'STRING': 'STRING',
    'IMPLEMENTATION': 'IMPLEMENTATION',
    'TRUE': 'TRUE',
    'FALSE': 'FALSE',
}

# Reglas para los tokens reservados y otros tokens
def t_IDENT(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDENT')
    return t

def t_STRING_LITERAL(t):
    r'\'(\'\'|[^'])*\''
    t.value = t.value[1:-1]
    return t

def t_NUM_REAL(t):
    r'\d+\.\d+([eE][+-]?\d+)?|\d+[eE][+-]?\d+'
    t.value = float(t.value)
    return t

def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_comment(t):
    r'\(\*.*?\*\)|\{.*?\}'
    pass

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición de la gramática
def p_program(p):
    '''program : programHeading INTERFACE block DOT
               | programHeading block DOT'''
    pass

def p_programHeading(p):
    '''programHeading : PROGRAM identifier LPAREN identifierList RPAREN SEMI
                      | PROGRAM identifier SEMI
                      | UNIT identifier SEMI'''
    pass

def p_identifier(p):
    'identifier : IDENT'
    pass

def p_block(p):
    '''block : labelDeclarationPart constantDefinitionPart typeDefinitionPart variableDeclarationPart procedureAndFunctionDeclarationPart usesUnitsPart IMPLEMENTATION compoundStatement
             | compoundStatement'''
    pass

def p_usesUnitsPart(p):
    'usesUnitsPart : USES identifierList SEMI'
    pass

def p_labelDeclarationPart(p):
    'labelDeclarationPart : LABEL labelList SEMI'
    pass

def p_labelList(p):
    'labelList : label COMMA labelList
               | label'
    pass

def p_label(p):
    'label : NUM_INT'
    pass

def p_constantDefinitionPart(p):
    'constantDefinitionPart : CONST constantDefinitionList'
    pass

def p_constantDefinitionList(p):
    'constantDefinitionList : constantDefinition SEMI constantDefinitionList
                            | constantDefinition SEMI'
    pass

def p_constantDefinition(p):
    'constantDefinition : identifier EQUAL constant'
    pass

def p_constant(p):
    '''constant : NUM_INT
                | NUM_REAL
                | identifier
                | PLUS constant
                | MINUS constant
                | STRING_LITERAL
                | constantChr'''
    pass

def p_constantChr(p):
    'constantChr : CHR LPAREN NUM_INT RPAREN'
    pass

def p_typeDefinitionPart(p):
    'typeDefinitionPart : TYPE typeDefinitionList'
    pass

def p_typeDefinitionList(p):
    'typeDefinitionList : typeDefinition SEMI typeDefinitionList
                        | typeDefinition SEMI'
    pass

def p_typeDefinition(p):
    '''typeDefinition : identifier EQUAL type_
                      | identifier EQUAL functionType
                      | identifier EQUAL procedureType'''
    pass

def p_functionType(p):
    'functionType : FUNCTION formalParameterList COLON resultType'
    pass

def p_procedureType(p):
    'procedureType : PROCEDURE formalParameterList'
    pass

def p_type_(p):
    '''type_ : simpleType
             | structuredType
             | pointerType'''
    pass

def p_simpleType(p):
    '''simpleType : scalarType
                  | subrangeType
                  | typeIdentifier
                  | stringtype'''
    pass

def p_scalarType(p):
    'scalarType : LPAREN identifierList RPAREN'
    pass

def p_subrangeType(p):
    'subrangeType : constant DOTDOT constant'
    pass

def p_typeIdentifier(p):
    '''typeIdentifier : identifier
                      | CHAR
                      | BOOLEAN
                      | INTEGER
                      | REAL
                      | STRING'''
    pass

def p_structuredType(p):
    '''structuredType : PACKED unpackedStructuredType
                      | unpackedStructuredType'''
    pass

def p_unpackedStructuredType(p):
    '''unpackedStructuredType : arrayType
                              | recordType
                              | setType
                              | fileType'''
    pass

def p_stringtype(p):
    'stringtype : STRING LBRACK identifier RBRACK'
    pass

def p_arrayType(p):
    '''arrayType : ARRAY LBRACK typeList RBRACK OF componentType
                 | ARRAY LBRACK2 typeList RBRACK2 OF componentType'''
    pass

def p_typeList(p):
    'typeList : indexType COMMA typeList | indexType'
    pass

def p_indexType(p):
    'indexType : simpleType'
    pass

def p_componentType(p):
    'componentType : type_'
    pass

def p_recordType(p):
    'recordType : RECORD fieldList END'
    pass

def p_fieldList(p):
    '''fieldList : fixedPart SEMI variantPart
                 | variantPart
                 | fixedPart'''
    pass

def p_fixedPart(p):
    'fixedPart : recordSection SEMI fixedPart | recordSection'
    pass

def p_recordSection(p):
    'recordSection : identifierList COLON type_'
    pass

def p_variantPart(p):
    'variantPart : CASE tag OF variantList END'
    pass

def p_tag(p):
    '''tag : identifier COLON typeIdentifier
           | typeIdentifier'''
    pass

def p_variantList(p):
    'variantList : variant SEMI variantList | variant'
    pass

def p_variant(p):
    'variant : constList COLON LPAREN fieldList RPAREN'
    pass

def p_setType(p):
    'setType : SET OF baseType'
    pass

def p_baseType(p):
    'baseType : simpleType'
    pass

def p_fileType(p):
    '''fileType : FILE OF type_
                | FILE'''
    pass

def p_pointerType(p):
    'pointerType : POINTER typeIdentifier'
    pass

def p_variableDeclarationPart(p):
    'variableDeclarationPart : VAR variableDeclaration SEMI variableDeclarationList'
    pass

def p_variableDeclarationList(p):
    'variableDeclarationList : variableDeclaration SEMI variableDeclarationList | variableDeclaration'
    pass

def p_variableDeclaration(p):
    'variableDeclaration : identifierList COLON type_'
    pass

def p_procedureAndFunctionDeclarationPart(p):
    'procedureAndFunctionDeclarationPart : procedureOrFunctionDeclaration SEMI'
    pass

def p_procedureOrFunctionDeclaration(p):
    '''procedureOrFunctionDeclaration : procedureDeclaration
                                      | functionDeclaration'''
    pass

def p_procedureDeclaration(p):
    'procedureDeclaration : PROCEDURE identifier formalParameterList SEMI block'
    pass

def p_functionDeclaration(p):
    'functionDeclaration : FUNCTION identifier formalParameterList COLON resultType SEMI block'
    pass

def p_formalParameterList(p):
    'formalParameterList : LPAREN formalParameterSection SEMI formalParameterSectionList RPAREN | LPAREN formalParameterSection RPAREN'
    pass

def p_formalParameterSectionList(p):
    'formalParameterSectionList : formalParameterSection SEMI formalParameterSectionList | formalParameterSection'
    pass

def p_formalParameterSection(p):
    '''formalParameterSection : parameterGroup
                              | VAR parameterGroup
                              | FUNCTION parameterGroup
                              | PROCEDURE parameterGroup'''
    pass

def p_parameterGroup(p):
    'parameterGroup : identifierList COLON typeIdentifier'
    pass

def p_identifierList(p):
    'identifierList : identifier COMMA identifierList | identifier'
    pass

def p_constList(p):
    'constList : constant COMMA constList | constant'
    pass

def p_resultType(p):
    'resultType : typeIdentifier'
    pass

def p_statement(p):
    '''statement : label COLON unlabelledStatement
                 | unlabelledStatement'''
    pass

def p_unlabelledStatement(p):
    '''unlabelledStatement : simpleStatement
                           | structuredStatement'''
    pass

def p_simpleStatement(p):
    '''simpleStatement : assignmentStatement
                       | procedureStatement
                       | gotoStatement
                       | emptyStatement_'''
    pass

def p_assignmentStatement(p):
    'assignmentStatement : variable ASSIGN expression'
    pass

def p_variable(p):
    '''variable : AT identifier
                | identifier
                | variable LBRACK expression RBRACK
                | variable LBRACK expression COMMA expression RBRACK
                | variable LBRACK2 expression RBRACK2
                | variable LBRACK2 expression COMMA expression RBRACK2
                | variable DOT identifier
                | variable POINTER'''
    pass

def p_expression(p):
    'expression : simpleExpression relationaloperator expression | simpleExpression'
    pass

def p_relationaloperator(p):
    '''relationaloperator : EQUAL
                          | NOT_EQUAL
                          | LT
                          | LE
                          | GE
                          | GT
                          | IN'''
    pass

def p_simpleExpression(p):
    'simpleExpression : term additiveoperator simpleExpression | term'
    pass

def p_additiveoperator(p):
    '''additiveoperator : PLUS
                        | MINUS
                        | OR'''
    pass

def p_term(p):
    'term : signedFactor multiplicativeoperator term | signedFactor'
    pass

def p_multiplicativeoperator(p):
    '''multiplicativeoperator : STAR
                              | SLASH
                              | DIV
                              | MOD
                              | AND'''
    pass

def p_signedFactor(p):
    'signedFactor : PLUS factor | MINUS factor | factor'
    pass

def p_factor(p):
    '''factor : variable
              : LPAREN expression RPAREN
              : functionDesignator
              : unsignedConstant
              : set_
              : NOT factor
              : bool_'''
    pass

def p_unsignedConstant(p):
    '''unsignedConstant : NUM_INT
                        : NUM_REAL
                        : STRING_LITERAL
                        : constantChr
                        : NIL'''
    pass

def p_functionDesignator(p):
    'functionDesignator : identifier LPAREN parameterList RPAREN'
    pass

def p_parameterList(p):
    'parameterList : actualParameter COMMA parameterList | actualParameter'
    pass

def p_set_(p):
    '''set_ : LBRACK elementList RBRACK
            : LBRACK2 elementList RBRACK2'''
    pass

def p_elementList(p):
    'elementList : element COMMA elementList | element | empty_'
    pass

def p_element(p):
    'element : expression DOTDOT expression | expression'
    pass

def p_procedureStatement(p):
    'procedureStatement : identifier LPAREN parameterList RPAREN | identifier'
    pass

def p_actualParameter(p):
    'actualParameter : expression parameterwidth | expression'
    pass

def p_parameterwidth(p):
    'parameterwidth : COLON expression'
    pass

def p_gotoStatement(p):
    'gotoStatement : GOTO label'
    pass

def p_emptyStatement_(p):
    'emptyStatement_ :'
    pass

def p_empty_(p):
    'empty_ :'
    pass

def p_structuredStatement(p):
    '''structuredStatement : compoundStatement
                           | conditionalStatement
                           | repetitiveStatement
                           | withStatement'''
    pass

def p_compoundStatement(p):
    'compoundStatement : BEGIN statements END'
    pass

def p_statements(p):
    'statements : statement SEMI statements | statement'
    pass

def p_conditionalStatement(p):
    '''conditionalStatement : ifStatement
                            : caseStatement'''
    pass

def p_ifStatement(p):
    'ifStatement : IF expression THEN statement ELSE statement | IF expression THEN statement'
    pass

def p_caseStatement(p):
    'caseStatement : CASE expression OF caseListElement SEMI caseListElementList ELSE statements END | CASE expression OF caseListElement SEMI caseListElementList END'
    pass

def p_caseListElementList(p):
    'caseListElementList : caseListElement SEMI caseListElementList | caseListElement'
    pass

def p_caseListElement(p):
    'caseListElement : constList COLON statement'
    pass

def p_repetitiveStatement(p):
    '''repetitiveStatement : whileStatement
                           : repeatStatement
                           : forStatement'''
    pass

def p_whileStatement(p):
    'whileStatement : WHILE expression DO statement'
    pass

def p_repeatStatement(p):
    'repeatStatement : REPEAT statements UNTIL expression'
    pass

def p_forStatement(p):
    'forStatement : FOR identifier ASSIGN forList DO statement'
    pass

def p_forList(p):
    'forList : initialValue TO finalValue | initialValue DOWNTO finalValue'
    pass

def p_initialValue(p):
    'initialValue : expression'
    pass

def p_finalValue(p):
    'finalValue : expression'
    pass

def p_withStatement(p):
    'withStatement : WITH recordVariableList DO statement'
    pass

def p_recordVariableList(p):
    'recordVariableList : variable COMMA recordVariableList | variable'
    pass

def p_bool_(p):
    '''bool_ : TRUE
             : FALSE'''
    pass

# Manejo de errores
def p_error(p):
    print(f"Syntax error at {p.value}")

parser = yacc.yacc()

# Ejemplo de uso
data = '''
program Example;
begin
    writeln('Hello, world!');
end.
'''

parser.parse(data)
