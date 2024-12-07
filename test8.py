# Prueba de Integración - Proyecto 3
from Proyecto3 import (
    Leer_codigo, Contar_lineas_fisicas, Contar_lineas_logicas, Imprimir_bloques,
    Contar_lineas_totales, detectar_urls_o_direcciones
)

# Crea los archivos de prueba a partir de los escenarios previamente definidos
def crear_archivos_prueba():
    casos_prueba = {
        "test_integracion.py": '''
# Integración de varias estructuras
def funcion_a():
    pass

def funcion_b():
    pass

if __name__ == "__main__":
    print("Bloque principal")
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

# Ejecuta la prueba de integración
def ejecutar_prueba(archivo, descripcion):
    print(f"\nEjecutando prueba de integración: {descripcion} ({archivo})")
    try:
        # Leer el archivo como una lista de líneas
        with open(archivo, "r") as file:
            lineas = file.readlines()

        # Llamada a la función de Leer_codigo
        print("- Leyendo código y dividiendo en funciones y bloques...")
        funciones, bloque_principal, lineas_completas = Leer_codigo(lineas)
        
        # Imprimir las funciones y el bloque principal
        Imprimir_bloques(funciones, bloque_principal)

        # Contar líneas físicas y lógicas
        print("- Contando líneas físicas y lógicas...")
        Contar_lineas_totales(lineas_completas)

        # Verificar si hay URLs o direcciones en el archivo
        print("- Verificando URLs y direcciones...")
        for linea in lineas:
            if detectar_urls_o_direcciones(linea):
                print(f"  URL o dirección detectada: {linea.strip()}")

    except Exception as e:
        print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    # Crear archivos de prueba automáticamente
    crear_archivos_prueba()

    # Archivos de prueba con descripciones
    pruebas = [
        ("test_integracion.py", "Prueba de integración: Funciones, estructuras lógicas y bloque principal")
    ]

    # Ejecutar todas las pruebas
    for archivo, descripcion in pruebas:
        ejecutar_prueba(archivo, descripcion)
