# Prueba proyecto 2
from Proyecto2 import Verificar_estandares_archivo, Contar_lineas_fisicas, Contar_lineas_logicas, Leer_codigo, Imprimir_bloques, Contar_lineas_totales

# Crea los archivos de prueba a partir de los escenarios previamente definidos
def crear_archivos_prueba():
    casos_prueba = {
        "test_comentarios.py": '''
# Este es un comentario simple
# Otro comentario más

# Más comentarios después de una línea vacía
''',
        "test_declaraciones.py": '''
# Declaraciones de variables y asignaciones

a = 10  # Comentario en línea
b = 20
c = a + b

# Impresiones en consola
print("Resultado:", c)
print("Fin del programa")
''',
        "test_importaciones.py": '''
# Importaciones de librerías y archivos externos

import os
import sys
from math import sqrt
from datetime import datetime
''',
        "test_logicas.py": '''
# Funciones, sentencias lógicas, docstrings y comentarios

def Suma(a, b):
    """Esta función suma dos números."""  
    return a + b

if __name__ == "__main__":
    resultado = Suma(5, 10)
    print(f"Resultado: {resultado}")

    for i in range(5):
        if i % 2 == 0:
            print(f"{i} es par")
        else:
            print(f"{i} es impar")
''',
        "test_completo.py": '''
# Este archivo combina todos los casos de prueba anteriores

# Comentarios simples y multilínea
# Este es un comentario simple

# Declaraciones de variables y asignaciones
a = 10
b = 20
resultado = a + b

# Importaciones
import os
from math import sqrt

# Funciones y sentencias lógicas
def Suma(a, b):
    # Función que suma dos números.
    return a + b

if __name__ == "__main__":
    print("Programa suma")
    print(f"Suma: {Suma(a, b)}")
    for i in range(3):
        if i % 2 == 0:
            print(f"{i} es par")
        else:
            print(f"{i} es impar")
'''
    }

    # Escribir los archivos de prueba
    for nombre_archivo, contenido in casos_prueba.items():
        with open(nombre_archivo, "w") as archivo:
            archivo.write(contenido)

# Ejecuta una prueba con un archivo y descripción
def ejecutar_prueba(archivo, descripcion):
    print(f"\nEjecutando prueba: {descripcion} ({archivo})")
    try:
        # Leer el archivo como una lista de líneas
        with open(archivo, "r") as file:
            lineas = file.readlines()  # Lee el archivo línea por línea

        print("- Contando líneas físicas...")
        lineas_fisicas = Contar_lineas_fisicas(lineas)  # Ahora pasas las líneas leídas
        print(f"  Líneas físicas: {lineas_fisicas}")

        # Aquí también podrías contar las líneas lógicas si lo deseas
        # print("- Contando líneas lógicas...")
        # lineas_logicas = Contar_lineas_logicas(archivo)
        # print(f"  Líneas lógicas: {lineas_logicas}")

    except Exception as e:
        print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    # Crear archivos de prueba automáticamente
    crear_archivos_prueba()

    # Archivos de prueba con descripciones
    pruebas = [
        ("test_comentarios.py", "Caso 1: Comentarios simples y multilínea"),
        ("test_declaraciones.py", "Caso 2: Declaraciones y asignaciones"),
        ("test_importaciones.py", "Caso 3: Importaciones de librerías"),
        ("test_logicas.py", "Caso 4: Funciones y sentencias lógicas"),
        ("test_completo.py", "Caso 5: Caso completo"),
    ]

    # Ejecutar todas las pruebas
    for archivo, descripcion in pruebas:
        ejecutar_prueba(archivo, descripcion)
