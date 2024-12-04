import tkinter as tk   
from tkinter import filedialog 
from tabulate import tabulate


# Función para leer el código desde un archivo y dividirlo en funciones y bloque principal
def Leer_codigo(filename):
    with open(filename, 'r') as file:

        lines = file.readlines()  # Lee todas las líneas del archivo

    funciones = []  # Lista para almacenar las funciones encontradas
    funcion_actual = []  # Almacena las líneas de la función que se está procesando
    bloque_principal = []  # Almacena las líneas del bloque principal del programa
    dentro_de_funcion = False  # Indica si estamos dentro de una función
    dentro_de_main = False  # Indica si estamos dentro del bloque principal
    nombre_funcion_actual = ""  # Almacena el nombre de la función actual

    for line in lines:
        stripped_line = line.strip()  # Elimina espacios en blanco al inicio y al final de la línea

        # Detecta el inicio de una función
        if stripped_line.startswith('def ') and not dentro_de_main:

            if dentro_de_funcion:  # Si ya estábamos procesando una función, la guarda
                funciones.append((nombre_funcion_actual, funcion_actual))
                funcion_actual = []  # Reinicia el contenido de la función actual

            dentro_de_funcion = True
            nombre_funcion_actual = stripped_line.split('(')[0][4:]  # Extrae el nombre de la función

        # Detecta el inicio del bloque principal
        if stripped_line.startswith('if __name__ == "__main__":'):

            if dentro_de_funcion:  # Guarda cualquier función no guardada antes de entrar al bloque principal
                funciones.append((nombre_funcion_actual, funcion_actual))
                funcion_actual = []

            dentro_de_main = True
            dentro_de_funcion = False

        # Añade líneas a la función o al bloque principal según corresponda
        if dentro_de_funcion:
            funcion_actual.append(line)

        elif dentro_de_main:
            bloque_principal.append(line)

    if funcion_actual:  # Si queda alguna función por guardar, la añade
        funciones.append((nombre_funcion_actual, funcion_actual))

    return funciones, bloque_principal, lines


# Función para contar líneas físicas (líneas no vacías ni comentarios)
def Contar_lineas_fisicas(codigo):
    lineas_validas = []

    for linea in codigo:
        linea_strip = linea.strip()

        if linea_strip and not linea_strip.startswith("#"):  # Ignora comentarios y líneas vacías
            lineas_validas.append(linea_strip)

    return len(lineas_validas)

# Función para contar líneas lógicas (líneas que representan instrucciones clave)
def Contar_lineas_logicas(codigo):
    palabras_clave = {"if", "for", "while", "def", "try", "with", "class"}  # Instrucciones clave
    lineas_logicas = 0

    for linea in codigo:
        linea_strip = linea.strip()

        if linea_strip:
            es_comentario = linea_strip.startswith("#")  # Verifica si es un comentario

            if not es_comentario:
                inicia_con_palabra_clave = False

                for palabra in palabras_clave:

                    if linea_strip.startswith(palabra):  # Verifica si la línea comienza con una palabra clave
                        inicia_con_palabra_clave = True
                        break

                if inicia_con_palabra_clave:
                    lineas_logicas += 1

    return lineas_logicas


# Función para imprimir las funciones y el bloque principal en formato tabular
def Imprimir_bloques(funciones, bloque_principal):
    datos = []  # Lista para almacenar los datos a mostrar en la tabla
    total_loc_programa = 0  # Contador para el total de LOC físicas del programa

    # Procesa cada función
    for i, (nombre, funcion) in enumerate(funciones):

        lineas_fisicas = Contar_lineas_fisicas(funcion)
        lineas_logicas = Contar_lineas_logicas(funcion)
        total_loc_programa += lineas_fisicas
        datos.append([f"Función {i + 1}", nombre, 1, lineas_fisicas, lineas_logicas])

    # Añade los datos del bloque principal
    lineas_fisicas_principal = Contar_lineas_fisicas(bloque_principal)
    lineas_logicas_principal = Contar_lineas_logicas(bloque_principal)
    total_loc_programa += lineas_fisicas_principal
    datos.append(["Bloque Principal", "", "", lineas_fisicas_principal, lineas_logicas_principal])

    # Imprime los datos en formato de tabla
    encabezados = ["Programa", "Función / Procedimiento", "Total de métodos", "LOC físicas", "LOC lógicas"]
    print(tabulate(datos, headers=encabezados, tablefmt="grid", stralign="center"))


# Función para contar e imprimir el total de líneas físicas y lógicas del programa
def Contar_lineas_totales(codigo):
    lineas_fisicas_totales = Contar_lineas_fisicas(codigo)
    lineas_logicas_totales = Contar_lineas_logicas(codigo)

    print("\nTotales del código completo:")
    print(f"Líneas físicas: {lineas_fisicas_totales}")
    print(f"Líneas lógicas: {lineas_logicas_totales}")


# Bloque principal: Punto de entrada del programa
if __name__ == "__main__":
    # Crea una ventana oculta para abrir el cuadro de diálogo de selección de archivos
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    # Abre un cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")])

    if archivo:  # Verifica si el usuario seleccionó un archivo

        try:
            # Lee el archivo y procesa el contenido
            funciones, bloque_principal, lines = Leer_codigo(archivo)
            Imprimir_bloques(funciones, bloque_principal)
            Contar_lineas_totales(lines)

        except FileNotFoundError:
            # Maneja el error en caso de que la ruta del archivo no sea válida
            print("Error: No se pudo encontrar el archivo. Verifica la ruta seleccionada.")

        except Exception as e:
            # Maneja otros errores inesperados
            print(f"Ha ocurrido un error: {e}")

    else:
        print("No se seleccionó ningún archivo.")
