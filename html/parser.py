import ply.lex as lex
import ply.yacc as yacc

# Lexer tokens and states
tokens = (
    'HTML_COMMENT', 'HTML_CONDITIONAL_COMMENT', 'XML', 'CDATA', 'DTD',
    'SCRIPTLET', 'SEA_WS', 'SCRIPT_OPEN', 'STYLE_OPEN', 'TAG_OPEN',
    'HTML_TEXT', 'TAG_CLOSE', 'TAG_SLASH_CLOSE', 'TAG_SLASH',
    'TAG_EQUALS', 'TAG_NAME', 'SCRIPT_BODY', 'STYLE_BODY', 'ATTVALUE_VALUE'
)

states = (
    ('tag', 'exclusive'),
    ('script', 'exclusive'),
    ('style', 'exclusive'),
    ('attvalue', 'exclusive')
)

t_ignore = ' \t'

def t_HTML_COMMENT(t):
    r'<!--.*?-->'
    return t

def t_HTML_CONDITIONAL_COMMENT(t):
    r'<!\[.*?\]>'
    return t

def t_XML(t):
    r'<\?xml.*?\?>'
    return t

def t_CDATA(t):
    r'<!\[CDATA\[.*?\]\]>'
    return t

def t_DTD(t):
    r'<!.*?>'
    return t

def t_SCRIPTLET(t):
    r'<\?.*?\?>|<%.*?%>'
    t.value = t.value.strip('<%>').strip() # Clean the scriptlet content
    return t

def t_SEA_WS(t):
    r'[ \t]+'
    return t

def t_SCRIPT_OPEN(t):
    r'<script.*?>'
    t.lexer.begin('script')
    return t

def t_STYLE_OPEN(t):
    r'<style.*?>'
    t.lexer.begin('style')
    return t

def t_TAG_OPEN(t):
    r'<'
    t.lexer.begin('tag')
    return t

def t_HTML_TEXT(t):
    r'[^<]+'
    return t

# Tag state rules
def t_tag_TAG_CLOSE(t):
    r'>'
    t.lexer.begin('INITIAL')
    return t

def t_tag_TAG_SLASH_CLOSE(t):
    r'/>'
    t.lexer.begin('INITIAL')
    return t

def t_tag_TAG_SLASH(t):
    r'/'
    return t

def t_tag_TAG_EQUALS(t):
    r'='
    t.lexer.begin('attvalue')
    return t

def t_tag_TAG_NAME(t):
    r'[a-zA-Z_:][a-zA-Z0-9_:.\u00B7\u0300-\u036F\u203F-\u2040]*'
    return t

def t_tag_TAG_WHITESPACE(t):
    r'[ \t\r\n]+'
    return t

t_tag_ignore = ' \t\r\n'

def t_tag_error(t):
    print(f"Unexpected character in 'tag' state: {t.value[0]}")
    t.lexer.skip(1)

# Script state rules
def t_script_SCRIPT_BODY(t):
    r'[^<]+'
    return t

def t_script_TAG_CLOSE(t):
    r'</script>'
    t.lexer.begin('INITIAL')
    return t

t_script_ignore = ' \t\r\n'

def t_script_error(t):
    print(f"Unexpected character in 'script' state: {t.value[0]}")
    t.lexer.skip(1)

# Style state rules
def t_style_STYLE_BODY(t):
    r'[^<]+'
    return t

def t_style_TAG_CLOSE(t):
    r'</style>'
    t.lexer.begin('INITIAL')
    return t

t_style_ignore = ' \t\r\n'

def t_style_error(t):
    print(f"Unexpected character in 'style' state: {t.value[0]}")
    t.lexer.skip(1)

# Attvalue state rules
def t_attvalue_ATTVALUE_VALUE(t):
    r'[^<>]+'
    t.lexer.begin('tag')
    return t

t_attvalue_ignore = ' \t\r\n'

def t_attvalue_error(t):
    print(f"Unexpected character in 'attvalue' state: {t.value[0]}")
    t.lexer.skip(1)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser rules
def p_html(p):
    '''html : elements'''
    p[0] = ('html', p[1])

def p_elements(p):
    '''elements : elements element
                | element'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_element(p):
    '''element : text
               | comment
               | conditional_comment
               | xml
               | cdata
               | dtd
               | script
               | style
               | tag'''
    p[0] = p[1]

def p_text(p):
    '''text : HTML_TEXT'''
    p[0] = ('text', p[1])

def p_comment(p):
    '''comment : HTML_COMMENT'''
    p[0] = ('comment', p[1])

def p_conditional_comment(p):
    '''conditional_comment : HTML_CONDITIONAL_COMMENT'''
    p[0] = ('conditional_comment', p[1])

def p_xml(p):
    '''xml : XML'''
    p[0] = ('xml', p[1])

def p_cdata(p):
    '''cdata : CDATA'''
    p[0] = ('cdata', p[1])

def p_dtd(p):
    '''dtd : DTD'''
    p[0] = ('dtd', p[1])

# Add a parser rule to handle SCRIPTLET tokens
def p_scriptlet(p):
    '''element : SCRIPTLET'''
    p[0] = ('scriptlet', p[1])  # Capture scriptlet content

# Add a parser rule to handle SEA_WS tokens
def p_sea_ws(p):
    '''element : SEA_WS'''
    p[0] = ('sea_ws', p[1]) # Capture SEA_WS content
    
def p_script(p):
    '''script : SCRIPT_OPEN script_body SCRIPT_CLOSE'''
    p[0] = ('script', p[2])

def p_script_body(p):
    '''script_body : SCRIPT_BODY'''
    p[0] = p[1]

def p_script_close(p):
    '''SCRIPT_CLOSE : TAG_OPEN TAG_SLASH TAG_NAME TAG_CLOSE'''
    p[0] = ('/script',)

def p_style(p):
    '''style : STYLE_OPEN style_body STYLE_CLOSE'''
    p[0] = ('style', p[2])

def p_style_body(p):
    '''style_body : STYLE_BODY'''
    p[0] = p[1]

def p_style_close(p):
    '''STYLE_CLOSE : TAG_OPEN TAG_SLASH TAG_NAME TAG_CLOSE'''
    p[0] = ('/style',)

def p_tag(p):
    '''tag : TAG_OPEN tag_name tag_attributes TAG_CLOSE
           | TAG_OPEN tag_name tag_attributes TAG_SLASH_CLOSE
           | TAG_OPEN TAG_SLASH tag_name TAG_CLOSE '''
    if len(p) == 5:  
        p[0] = ('tag', p[2], p[3])  
    else:
        p[0] = ('/', p[3])  

def p_tag_name(p):
    '''tag_name : TAG_NAME'''
    p[0] = p[1]

def p_tag_attributes(p):
    '''tag_attributes : tag_attributes tag_attribute
                      | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_tag_attribute(p):
    '''tag_attribute : TAG_NAME TAG_EQUALS attribute_value'''
    p[0] = (p[1], p[3])

def p_attribute_value(p):
    '''attribute_value : ATTVALUE_VALUE'''
    p[0] = p[1]

# ... (lexer definitions remain the same)

# Parser Enhancements
def p_tag_close(p):
    '''tag_close : TAG_CLOSE
                 | TAG_SLASH_CLOSE'''
    if len(p) == 2:
        p[0] = ('/',)  # Indicate self-closing tag
    else:
        p[0] = ()      # Regular closing tag

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' in line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# Ejemplo de uso
data = '''
<!DOCTYPE html>
<html>
    <head>
    <title>Title of the document</title>
    </head>
    <body>
        <h1>This is a heading</h1>
        <p>This is a paragraph.</p>
    </body>
</html>
'''

lexer.input(data)
for tok in lexer:
    print(tok)

result = parser.parse(data, lexer=lexer)
print(result)


