from lexico import lexer
from parser import parser

# Cadena de prueba
test_string = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <script>
        console.log("Hello, world!");
    </script>
    <style>
        body {background-color: #d0e4fe;}
    </style>
</head>
<body>
    <!-- This is a comment -->
    <h1>This is a heading</h1>
    <p>This is a paragraph.</p>
</body>
</html>
'''

# Analizar el lexer
lexer.input(test_string)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

# Analizar el parser
result = parser.parse(test_string, lexer=lexer)
print(result)
