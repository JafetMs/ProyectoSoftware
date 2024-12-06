from proyecto1 import Verificar_estandares_archivo, Contar_lineas_fisicas, Contar_lineas_logicas

# Definir las pruebas para cada escenario
def crear_archivos_prueba():
    casos_prueba = {
        "test_escenario_1.py": '''
# Esto es un comentario
# Otro comentario

# Línea vacía

a = 10
b = 5
''',

        "test_escenario_2.py": '''
# Declaraciones y asignaciones
x = 1
y = 2
print(x + y)

# Más declaraciones
z = x * y
''',

        "test_escenario_3.py": '''
# Importación de librerías
import math
import sys

# Declaración de función
def saludo():
    print("Hola Mundo")

x = 0
y = 9

z = x + y
# Es un comentario 
print("Hola) 
''',

        "test_escenario_4.py": '''
# Combinación de todos los escenarios anteriores
import math
import sys

# Declaración de función
def saludo():
    print("Hola Mundo")

x = 1
y = 2
print(x + y)

# Comentarios y líneas vacías
# Comentario 1
# Comentario 2
''',
    }

    # Crear archivos con el contenido de prueba
    for nombre_archivo, contenido in casos_prueba.items():
        with open(nombre_archivo, "w") as archivo:
            archivo.write(contenido)


# Ejecuta una prueba con un archivo y descripción
def ejecutar_prueba(archivo, descripcion, esperado_fisico, esperado_logico):
    print(f"\nEjecutando prueba: {descripcion} ({archivo})")
    try:
        ## Verificar estándares
        #print("- Verificando estándares...")
        #Verificar_estandares_archivo(archivo)
        #print("  ✓ Cumple con los estándares.")

        # Contar líneas físicas
        print("- Contando líneas físicas...")
        lineas_fisicas = Contar_lineas_fisicas(archivo)
        print(f"  Líneas físicas: {lineas_fisicas}")

        # Contar líneas lógicas
        print("- Contando líneas lógicas...")
        lineas_logicas = Contar_lineas_logicas(archivo)
        print(f"  Líneas lógicas: {lineas_logicas}")

        

    except Exception as e:
        print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    # Crear archivos de prueba automáticamente
    crear_archivos_prueba()

    # Definir las pruebas con las expectativas de líneas físicas y lógicas
    pruebas = [
        ("test_escenario_1.py", "Escenario 1: Comentarios y líneas vacías", 5, 0),  # 5 líneas físicas, 0 lógicas
        ("test_escenario_2.py", "Escenario 2: Declaraciones y asignaciones", 5, 3),  # 5 líneas físicas, 3 lógicas
        ("test_escenario_3.py", "Escenario 3: Importaciones y declaraciones", 7, 3),  # 7 líneas físicas, 3 lógicas
        ("test_escenario_4.py", "Escenario 4: Combinación de todos los elementos", 12, 6),  # 12 líneas físicas, 6 lógicas
    ]

    # Ejecutar todas las pruebas
    for archivo, descripcion, esperado_fisico, esperado_logico in pruebas:
        ejecutar_prueba(archivo, descripcion, esperado_fisico, esperado_logico)
