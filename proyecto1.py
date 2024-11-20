import tkinter as tk
from tkinter import filedialog

"""
  Programa para contar líneas lógicas y líneas físicas en un archivo
  de código fuente. Este programa excluye comentarios y líneas en
  blanco al contar las líneas lógicas.

  Estándares aplicados:
  - Líneas Lógicas: Se cuentan solo las líneas con código ejecutable 
    (se omiten comentarios y líneas en blanco).
  - Líneas Físicas: Se cuentan todas las líneas presentes en el 
    archivo, incluyendo comentarios y líneas en blanco.
"""

def contar_loc(file_path):
    """
      Cuenta las líneas lógicas y físicas en un archivo de código fuente.

      Args:
          file_path (str): Ruta del archivo que se desea analizar.

      Returns:
          tuple: Una tupla que contiene:
              - lineas_logicas (int): Número de líneas lógicas.
              - lineas_fisicas (int): Número de líneas físicas.
    """
    lineas_logicas = 0
    lineas_fisicas = 0

    with open(file_path, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            lineas_fisicas += 1
            linea_strip = linea.strip()
            if linea_strip and not linea_strip.startswith('#'):
                lineas_logicas += 1

    return lineas_logicas, lineas_fisicas


if __name__ == "__main__":
    """
      Bloque principal del programa. Permite ejecutar la función
      `contar_loc` para analizar un archivo, mostrando el resultado
      al usuario.
    """
    root = tk.Tk()
    root.withdraw()

    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")]
    )

    if archivo:
        try:
            #  Procesa el archivo seleccionado.
            loc_logicas, loc_fisicas = contar_loc(archivo)

            #  Muestra los resultados.
            print(f"Líneas Lógicas: {loc_logicas}")
            print(f"Líneas Físicas: {loc_fisicas}")

        except FileNotFoundError:
            print("Error: No se pudo encontrar el archivo.")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

    else:
        print("No se seleccionó ningún archivo.")
