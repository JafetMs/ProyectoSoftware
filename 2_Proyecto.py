import tkinter as tk
from tkinter import filedialog
from proyecto1 import contar_loc  # Importa la función del programa 1

def analizar_archivo(file_path):
    """
    Analiza el archivo seleccionado para contar:
    - Líneas físicas totales.
    - Líneas por clase.
    - Total de métodos por clase.

    Args:
        file_path (str): Ruta del archivo a analizar.
    
    Returns:
        dict: Un diccionario con las estadísticas del análisis.
    """
    estadisticas = {
        "total_lineas_fisicas": 0,
        "clases": []
    }

    with open(file_path, 'r') as archivo:
        lineas = archivo.readlines()
        estadisticas["total_lineas_fisicas"] = len(lineas)  # Cuenta las líneas físicas totales

        clase_actual = None
        metodos_en_clase = 0
        lineas_en_clase = 0

        for linea in lineas:
            linea_strip = linea.strip()

            # Detecta el inicio de una clase
            if linea_strip.startswith("class "):  # Ejemplo: class MiClase:
                if clase_actual:
                    # Si ya hay una clase activa, guarda las estadísticas
                    estadisticas["clases"].append({
                        "nombre": clase_actual,
                        "lineas": lineas_en_clase,
                        "metodos": metodos_en_clase
                    })

                # Reinicia las estadísticas para la nueva clase
                clase_actual = linea_strip.split("class")[1].split(":")[0].strip()
                metodos_en_clase = 0
                lineas_en_clase = 0

            # Detecta métodos dentro de la clase
            elif linea_strip.startswith("def ") and clase_actual:
                metodos_en_clase += 1

            # Cuenta líneas dentro de una clase
            if clase_actual:
                lineas_en_clase += 1

        # Agrega la última clase al finalizar
        if clase_actual:
            estadisticas["clases"].append({
                "nombre": clase_actual,
                "lineas": lineas_en_clase,
                "metodos": metodos_en_clase
            })

    return estadisticas


if __name__ == "__main__":
    """
    Bloque principal del programa para seleccionar un archivo y analizarlo.
    """
    # Crea una ventana oculta para abrir el cuadro de diálogo
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    # Abre una ventana para seleccionar un archivo
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")]
    )

    if archivo:  # Verifica si el usuario seleccionó un archivo
        try:
            # Llama a la función del programa 1 para contar las líneas lógicas y físicas
            lineas_logicas, lineas_fisicas = contar_loc(archivo)
            print(f"Líneas Físicas (todas las líneas): {lineas_fisicas}")

            # Analiza el archivo para contar clases y métodos
            resultado = analizar_archivo(archivo)

            print("\n--- Análisis de Clases ---")
            for clase in resultado["clases"]:
                print(f"Clase: {clase['nombre']}")
                print(f"  Líneas en la clase: {clase['lineas']}")
                print(f"  Métodos en la clase: {clase['metodos']}")

            print(f"\nTotal de líneas físicas en el programa: {resultado['total_lineas_fisicas']}")

        except FileNotFoundError:
            print("Error: No se pudo encontrar el archivo. Verifica la ruta seleccionada.")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")
    else:
        print("No se seleccionó ningún archivo.")
