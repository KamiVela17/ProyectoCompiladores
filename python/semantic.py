# Contexto global para almacenar información sobre funciones y variables
context = {}

# Excepción personalizada para errores semánticos
# En el módulo semantic.py

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Funciones semánticas

def check_function_defined(name):
    """
    Verifica si una función ya ha sido definida en el contexto.
    """
    if name in context:
        raise SemanticError(f"Function '{name}' already defined.")

def add_function_to_context(name, parameters):
    """
    Añade una nueva función al contexto.
    """
    context[name] = {'type': 'function', 'parameters': parameters, 'defined': True}

def check_variable_in_context(name):
    """
    Verifica si una variable ha sido definida en el contexto.
    """
    if name not in context:
        raise SemanticError(f"Variable '{name}' not defined.")

def add_variable_to_context(name, value):
    """
    Añade una nueva variable al contexto o actualiza una existente.
    """
    if name in context and context[name]['type'] == 'function':
        raise SemanticError(f"Cannot assign to function '{name}'.")
    context[name] = {'type': 'variable', 'value': value}

def check_assignment_to_function(name):
    """
    Verifica si se intenta asignar un valor a una función.
    """
    if name in context and context[name]['type'] == 'function':
        raise SemanticError(f"Cannot assign to function '{name}'.")

def check_type_mismatch(expected_type, actual_value):
    """
    Verifica si hay una discrepancia de tipo entre un valor esperado y uno actual.
    """
    if isinstance(actual_value, expected_type):
        return
    else:
        raise SemanticError(f"Type mismatch: Expected {expected_type}, got {type(actual_value).__name__}.")

def check_division_by_zero(divisor):
    """
    Verifica la división por cero.
    """
    if divisor == 0:
        raise SemanticError("Division by zero.")

def update_context_for_return(function_name, return_value):
    """
    Actualiza el contexto con el valor de retorno de una función.
    """
    if function_name in context and context[function_name]['type'] == 'function':
        context[function_name]['return_value'] = return_value
    else:
        raise SemanticError(f"'{function_name}' is not a function or not defined.")