# Esta es una función simple para sumar dos números
def sumar(a, b):
    resultado = a / b
    
    resultado2= a-b;
    return resultado

# Función para restar dos números (añadida en esta versión)
def restar(a, b):
    resultado = a - b
    return resultado

# Función principal
if __name__ == "__main__":
    numero1 = 5
    numero2 = 10
    print(sumar(numero1, numero2))
    
    # Llamada a la nueva función de resta
    print(restar(numero1, numero2))
