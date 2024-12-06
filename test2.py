from proyecto1 import Verificar_estandares_archivo, Contar_lineas_fisicas, Contar_lineas_logicas

# Crea los archivos de prueba para evaluar líneas lógicas
def crear_archivos_prueba():
    casos_prueba = {
        "test_if.py": '''
# Prueba para estructuras if
if a > b:
    print("a es mayor que b")
elif a == b:
    print("a es igual a b")
else:
    print("a es menor que b")
''',
        "test_for.py": '''
# Prueba para ciclos for
for i in range(10):
    print(i)
''',
        "test_while.py": '''
# Prueba para bucles while
while a < b:
    a += 1
    print(a)
''',
        "test_def.py": '''
# Prueba para funciones
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b
''',
        "test_class.py": '''
# Prueba para clases
class MiClase:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludo(self):
        return f"Hola, {self.nombre}"
''',
        "test_try.py": '''
# Prueba para bloques try-except
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Error: División por cero")
except Exception as e:
    print(f"Error inesperado: {e}")
''',
        "test_with.py": '''
# Prueba para bloques with
with open("archivo.txt", "w") as archivo:
    archivo.write("Contenido de prueba")
''',
        "test_combinado.py": '''
# Prueba combinada con todas las estructuras
if a > b:
    print("a es mayor que b")

for i in range(10):
    print(i)

while a < b:
    a += 1

def suma(a, b):
    return a + b

try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Error")

with open("archivo.txt", "w") as archivo:
    archivo.write("Contenido")
'''
    }

    for nombre_archivo, contenido in casos_prueba.items():
        with open(nombre_archivo, "w") as archivo:
            archivo.write(contenido)


# Ejecuta una prueba con un archivo y descripción
def ejecutar_prueba(archivo, descripcion):
    print(f"\nEjecutando prueba: {descripcion} ({archivo})")
    try:
        #print("- Verificando estándares...")
        #Verificar_estandares_archivo(archivo)
        #print("  ✓ Cumple con los estándares.")

        #print("- Contando líneas físicas...")
        #lineas_fisicas = Contar_lineas_fisicas(archivo)
        #print(f"  Líneas físicas: {lineas_fisicas}")

        print("- Contando líneas lógicas...")
        lineas_logicas = Contar_lineas_logicas(archivo)
        print(f"  Líneas lógicas: {lineas_logicas}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    # Crear archivos de prueba automáticamente
    crear_archivos_prueba()

    # Archivos de prueba con descripciones
    pruebas = [
        ("test_if.py", "Caso 1: Estructuras if"),
        ("test_for.py", "Caso 2: Ciclos for"),
        ("test_while.py", "Caso 3: Bucles while"),
        ("test_def.py", "Caso 4: Declaración de funciones (def)"),
        ("test_try.py", "Caso 5: Bloques try-except"),
        ("test_with.py", "Caso 6: Bloques with"),
        ("test_combinado.py", "Caso 7: Combinado con todas las estructuras"),
    ]

    # Ejecutar todas las pruebas
    for archivo, descripcion in pruebas:
        ejecutar_prueba(archivo, descripcion)
