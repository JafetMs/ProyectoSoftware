import tkinter as tk
from tkinter import filedialog

"""
Programa para contar líneas lógicas y líneas físicas en un archivo de código fuente.
Este programa excluye comentarios y líneas en blanco al contar las líneas lógicas.



Estándares aplicados:
- Líneas Lógicas: Se cuentan solo las líneas con código ejecutable (se omiten comentarios y líneas en blanco).
- Líneas Físicas: Se cuentan todas las líneas presentes en el archivo, incluyendo comentarios y líneas en blanco.
"""

def contar_loc(file_path):
    """
    Cuenta las líneas lógicas y físicas en un archivo de código fuente.

    Args:
        file_path (str): Ruta del archivo que se desea analizar.

    Returns:
        tuple: Una tupla que contiene:
            - lineas_logicas (int): Número de líneas lógicas (código ejecutable).
            - lineas_fisicas (int): Número de líneas físicas (todas las líneas).
    
    Detalles:
    - Una línea lógica es una línea que contiene código ejecutable.
    - Las líneas en blanco o que contienen solo comentarios (líneas que inician con `#`) no se cuentan como lógicas.
    - Todas las líneas del archivo (incluyendo en blanco y comentarios) se cuentan como físicas.
    """
    # Inicialización de contadores
    lineas_logicas = 0
    lineas_fisicas = 0

    # Abre el archivo en modo de solo lectura
    with open(file_path, 'r') as archivo:
        for linea in archivo:  # Itera por cada línea en el archivo
            lineas_fisicas += 1  # Incrementa el contador de líneas físicas por cada línea leída
            # Elimina espacios en blanco al inicio y final de la línea
            linea_strip = linea.strip()
            # Verifica si la línea no está vacía y no es un comentario
            if linea_strip and not linea_strip.startswith('#'):
                lineas_logicas += 1  # Incrementa el contador de líneas lógicas

    # Devuelve los contadores como una tupla
    return lineas_logicas, lineas_fisicas


if __name__ == "__main__":
    """
    Bloque principal del programa.

    Este bloque permite ejecutar la función `contar_loc` para analizar un archivo,
    mostrando el resultado al usuario.
    """
    # Crea una ventana oculta para abrir el cuadro de diálogo de selección de archivos
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    # Abre una ventana para seleccionar un archivo
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")]
    )

    if archivo:  # Verifica si el usuario seleccionó un archivo
        try:
            # Llama a la función para contar las líneas
            loc_logicas, loc_fisicas = contar_loc(archivo)

            # Muestra los resultados
            print(f"Líneas Lógicas: {loc_logicas}")
            print(f"Líneas Físicas: {loc_fisicas}")

        except FileNotFoundError:
            # Maneja el error en caso de que la ruta del archivo no sea válida
            print("Error: No se pudo encontrar el archivo. Verifica la ruta seleccionada.")
        except Exception as e:
            # Maneja otros errores inesperados
            print(f"Ha ocurrido un error: {e}")
    else:
        print("No se seleccionó ningún archivo.")
