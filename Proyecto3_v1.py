import os
import tkinter as tk
from tkinter import filedialog

def comparar_versiones(version_anterior, version_nueva):
    """Compara dos versiones de código y detecta líneas añadidas, eliminadas y movidas."""
    lineas_anterior = version_anterior.splitlines()
    lineas_nueva = version_nueva.splitlines()

    lineas_eliminadas = []
    lineas_añadidas = []

    # Detectar eliminaciones y añadidos considerando posición
    for i, linea_anterior in enumerate(lineas_anterior):
        if i >= len(lineas_nueva) or linea_anterior != lineas_nueva[i]:
            # Comentar completamente las líneas eliminadas si están fuera de bloques válidos
            if linea_anterior.strip() and linea_anterior.startswith(" "):
                # Verificar si la línea está fuera de una función o clase
                if not any(linea_anterior.strip().startswith(prefix) for prefix in ["def ", "class ", "if __name__ == '__main__'"]):
                    lineas_eliminadas.append(f"# {linea_anterior}  # Eliminada")
                else:
                    lineas_eliminadas.append(f"{linea_anterior}  # Eliminada")
            else:
                lineas_eliminadas.append(f"# {linea_anterior}  # Eliminada")
    
    for i, linea_nueva in enumerate(lineas_nueva):
        if i >= len(lineas_anterior) or linea_nueva != lineas_anterior[i]:
            # Comentar completamente las líneas añadidas si están fuera de bloques válidos
            if linea_nueva.strip() and linea_nueva.startswith(" "):
                # Verificar si la línea está fuera de una función o clase
                if not any(linea_nueva.strip().startswith(prefix) for prefix in ["def ", "class ", "if __name__ == '__main__'"]):
                    lineas_añadidas.append(f"# {linea_nueva}  # Añadida")
                else:
                    lineas_añadidas.append(f"{linea_nueva}  # Añadida")
            else:
                lineas_añadidas.append(f"# {linea_nueva}  # Añadida")

    return lineas_añadidas, lineas_eliminadas

def generar_reporte(version_anterior, version_nueva):
    """Genera un reporte de los cambios y guarda el resultado en un archivo."""
    lineas_añadidas, lineas_eliminadas = comparar_versiones(version_anterior, version_nueva)

    # Crear carpeta "resultado"
    if not os.path.exists("resultado"):
        os.makedirs("resultado")

    # Guardar el reporte
    ruta_resultado = os.path.join("resultado", "comparacion.py")
    with open(ruta_resultado, 'w', encoding='utf-8') as file:
        file.write("# Comparación de versiones\n\n")
        
        file.write("# Líneas añadidas:\n")
        for linea in lineas_añadidas:
            file.write(linea + "\n")
        
        file.write("\n# Líneas eliminadas:\n")
        for linea in lineas_eliminadas:
            file.write(linea + "\n")

    print(f"Archivo generado en: {ruta_resultado}")

def seleccionar_archivos():
    """Abre un cuadro de diálogo para seleccionar dos archivos."""
    root = tk.Tk()
    root.withdraw()

    archivo_anterior = filedialog.askopenfilename(title="Selecciona el archivo de la versión anterior", filetypes=[("Python Files", "*.py")])
    if not archivo_anterior:
        print("No se seleccionó archivo para la versión anterior.")
        return

    archivo_nueva = filedialog.askopenfilename(title="Selecciona el archivo de la versión nueva", filetypes=[("Python Files", "*.py")])
    if not archivo_nueva:
        print("No se seleccionó archivo para la versión nueva.")
        return

    with open(archivo_anterior, 'r', encoding='utf-8') as file:
        version_anterior = file.read()

    with open(archivo_nueva, 'r', encoding='utf-8') as file:
        version_nueva = file.read()

    generar_reporte(version_anterior, version_nueva)

if __name__ == "__main__":
    seleccionar_archivos()
