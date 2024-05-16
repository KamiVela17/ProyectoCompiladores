import ply.lex as lex

# Palabras reservadas
reserved = {
    'def': 'DEF',
    'return': 'RETURN',
}

# Lista de tokens
tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',
    'STRING',
    'EQUALS',
    'COMMA',
    'SEMICOLON',
    'FLOAT',
    'NEWLINE',  # Agregar token para manejar nuevas líneas
    'COLON',  # Agregar token para dos puntos
    'LBRACE',  # Agregar token para llave izquierda
    'RBRACE',  # Agregar token para llave derecha
] + list(reserved.values())

# Reglas para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Regla para identificadores y palabras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# Regla para números flotantes
def t_FLOAT(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

# Regla para números enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para cadenas de texto
def t_STRING(t):
    r'\".*?\"'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Regla para manejar comentarios
def t_COMMENT(t):
    r'\#.*'
    pass  # Token comentario no es devuelto

# Regla para saltos de línea
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
