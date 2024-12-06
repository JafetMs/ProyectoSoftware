# Prueba proyecto 2
from Proyecto2 import Verificar_estandares_archivo, Contar_lineas_fisicas, Contar_lineas_logicas, Leer_codigo, Imprimir_bloques, Contar_lineas_totales

# Crea los archivos de prueba a partir de los escenarios previamente definidos
def crear_archivos_prueba():
    casos_prueba = {
        "test_def.py": '''
# Prueba para funciones
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b
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
        funciones, bloque_principal, lines = Leer_codigo(archivo)
        Imprimir_bloques(funciones, bloque_principal)
        Contar_lineas_totales(lines)
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    # Crear archivos de prueba automáticamente
    crear_archivos_prueba()

    # Archivos de prueba con descripciones
    pruebas = [
        ("test_def.py", "Caso 4: Declaración de funciones (def)")
    ]

    # Ejecutar todas las pruebas
    for archivo, descripcion in pruebas:
        ejecutar_prueba(archivo, descripcion)
