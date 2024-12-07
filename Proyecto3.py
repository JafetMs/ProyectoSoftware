import tkinter as tk
from tkinter import filedialog
from tabulate import tabulate
import re


# Función para leer el código desde un archivo y dividirlo en funciones y bloque principal
def Leer_codigo(lineas):
    # Lista para almacenar las funciones encontradas
    # Almacena las líneas de la función que se está procesando
    # Almacena las líneas del bloque principal del programa
    # Indica si estamos dentro de una función
    # Indica si estamos dentro del bloque principal
    # Almacena el nombre de la función actual
    funciones = []  
    funcion_actual = []  
    bloque_principal = []  
    dentro_de_funcion = False  
    dentro_de_main = False  
    nombre_funcion_actual = "" 


    for linea in lineas:
        # Elimina espacios en blanco al inicio y al final de la línea
        stripped_line = linea.strip()  

        # Detecta el inicio de una función
        if stripped_line.startswith('def ') and not dentro_de_main:

            # Si ya estábamos procesando una función, la guarda
            if dentro_de_funcion:  
                funciones.append((nombre_funcion_actual, funcion_actual))
                # Reinicia el contenido de la función actual
                funcion_actual = []  

            dentro_de_funcion = True
            # Extrae el nombre de la función
            nombre_funcion_actual = stripped_line.split('(')[0][4:]  

        # Detecta el inicio del bloque principal
        if stripped_line.startswith('if __name__ == "__main__":'):

            # Guarda cualquier función no guardada antes de entrar al bloque principal
            if dentro_de_funcion:  
                funciones.append((nombre_funcion_actual, funcion_actual))
                funcion_actual = []

            dentro_de_main = True
            dentro_de_funcion = False

        # Añade líneas a la función o al bloque principal según corresponda
        if dentro_de_funcion:
            funcion_actual.append(linea)

        elif dentro_de_main:
            bloque_principal.append(linea)

    # Si queda alguna función por guardar, la añade
    if funcion_actual:  
        funciones.append((nombre_funcion_actual, funcion_actual))

    return funciones, bloque_principal, lineas


# Función para contar líneas físicas (líneas no vacías ni comentarios)
def Contar_lineas_fisicas(codigo):
    lineas_validas = []
    num_cambios = 0

    for linea in codigo:
        linea_strip = linea.strip()

        # Ignora comentarios y líneas vacías
        if linea_strip and not linea_strip.startswith("#"):

            if " \\ " in linea:
                num_cambios += 1  

            lineas_validas.append(linea_strip)

    return len(lineas_validas) - num_cambios

# Función para contar líneas lógicas (líneas que representan instrucciones clave)
def Contar_lineas_logicas(codigo):
    # Instrucciones clave
    palabras_clave = {"if", "for", "while", "def", "try", "with", }  
    lineas_logicas = 0

    for linea in codigo:
        linea_strip = linea.strip()

        if linea_strip:
            # Verifica si es un comentario
            es_comentario = linea_strip.startswith("#") 

            if not es_comentario:
                inicia_con_palabra_clave = False

                for palabra in palabras_clave:

                    # Verifica si la línea comienza con una palabra clave
                    if linea_strip.startswith(palabra):  
                        inicia_con_palabra_clave = True
                        break

                if inicia_con_palabra_clave:
                    lineas_logicas += 1

    return lineas_logicas


# Función para imprimir las funciones y el bloque principal en formato tabular
def Imprimir_bloques(funciones, bloque_principal):
    # Lista para almacenar los datos a mostrar en la tabla
    # Contador para el total de LOC físicas del programa
    datos = []  
    total_loc_programa = 0  

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
    # Ejecutar las funciones que cuentas las líneas físicas y lógicas
    # Imprime las líneas
    lineas_fisicas_totales = Contar_lineas_fisicas(codigo)
    lineas_logicas_totales = Contar_lineas_logicas(codigo)

    print("\nTotales del código completo:")
    print(f"Líneas físicas: {lineas_fisicas_totales}")
    print(f"Líneas lógicas: {lineas_logicas_totales}")


def Detectar_urls_o_direcciones(linea):
    # Expresión regular para detectar URLs
    url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    # Expresión regular mejorada para detectar direcciones de archivos
    # Windows
    # Unix/Linux
    # macOS
    file_path_regex = re.compile(
        r'([a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*)|'  
        r'(/(?:[^/\0]+/)*)|'  
        r'(/(?:[^/]+/)*[^/]+)'  
        )
    
    urls_encontradas = url_regex.findall(linea)
    archivos_encontrados = file_path_regex.findall(linea)
    
    return bool(urls_encontradas) or bool(archivos_encontrados)


# Función para cortar en más líneas aquellas líneas que superen los 80 caracteres
def Lineas_de_codigo(ruta_resultado):
    # Lista para almacenar las líneas ajustadas
    lineas_nuevas = []  

    # Abre el archivo y lee las líneas
    with open(ruta_resultado, 'r') as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        # Calcula la indentación de la línea actual
        indentacion = len(linea) - len(linea.lstrip())

        # Verifica si la línea es mayor a 80 caracteres, no es un comentario,
        # y no contiene URLs o direcciones
        if not Detectar_urls_o_direcciones(linea) and len(linea) > 80 and not linea.lstrip().startswith('#'):

            # Divide la línea en múltiples líneas mientras sea mayor a 80 caracteres
            while len(linea) > 80:
                # Busca el espacio más cercano al límite de 80 caracteres
                espacio_mas_cercano = linea.rfind(' ', 0, 79)

                # Si no hay espacio, corta en el carácter 79
                if espacio_mas_cercano == -1:
                    espacio_mas_cercano = 79 

                # Añade la primera parte con un indicador de continuación
                parte = linea[:espacio_mas_cercano].rstrip() + " \\ "
                lineas_nuevas.append(parte)

                # Ajusta la línea restante eliminando espacios iniciales
                linea = linea[espacio_mas_cercano:].lstrip()

            # Añade la última parte de la línea ajustada
            lineas_nuevas.append(' ' * indentacion + linea)

        else:
            # Si no necesita ajuste, añade la línea directamente
            lineas_nuevas.append(linea)

    # Escribe las líneas ajustadas de vuelta al archivo
    with open(ruta_resultado, 'w') as archivo:

        for linea in lineas_nuevas:
            archivo.write(f"{linea.rstrip()}\n")
    
    # Procesa el código ajustado para dividirlo en funciones y bloques principales
    funciones, bloque_principal, lineass = Leer_codigo(lineas_nuevas)
    # Imprime un resumen de las funciones y el bloque principal
    Imprimir_bloques(funciones, bloque_principal)
    # Cuenta las líneas totales del código ajustado
    Contar_lineas_totales(lineass)


# Función para comparar dos versiones de código y generar un archivo de diferencias
def Comparar_versiones(ruta_version_antigua, ruta_version_nueva):
    # Lee las líneas de ambas versiones en UTF-8
    with open(ruta_version_antigua, 'r', encoding='utf-8') as archivo:
        lineas_antiguas = archivo.readlines()

    with open(ruta_version_nueva, 'r', encoding='utf-8') as archivo:
        lineas_nuevas = archivo.readlines()

    # Contador de líneas añadidas
    lineas_añadidas = 0  
    # Contador de líneas borradas
    lineas_borradas = 0  

    # Crea el archivo de salida para registrar los cambios
    with open('output.py', 'w', encoding='utf-8') as archivo_salida:

        for linea in lineas_nuevas:

            if linea in lineas_antiguas:
                # Si la línea está en ambas versiones, simplemente la escribe
                archivo_salida.write(f"{linea.rstrip()}\n")

            else:
                # Si la línea es nueva, la marca como añadida
                archivo_salida.write("\n# Línea de abajo es añadida\n")
                archivo_salida.write(f"{linea.rstrip()}\n")
                lineas_añadidas += 1

        for linea in lineas_antiguas:
            
            if linea not in lineas_nuevas:
                # Si la línea no está en la nueva versión, la marca como borrada
                archivo_salida.write(f"# {linea.rstrip()}  # Línea borrada\n")
                lineas_borradas += 1

        # Calcula el total de cambios
        total_lineas = lineas_añadidas + lineas_borradas

        # Escribe el resumen de cambios al final del archivo
        archivo_salida.write(f"\n# Líneas añadidas: {lineas_añadidas}\n")
        archivo_salida.write(f"# Líneas borradas: {lineas_borradas}\n")
        archivo_salida.write(f"# Total de líneas: {total_lineas}\n")

    # Ajusta las líneas del archivo generado
    Lineas_de_codigo('output.py')


# Función para abrir un diálogo de selección de archivos
def Abrir_dialogo_archivo():
    raiz = tk.Tk()  # Crea una ventana de Tkinter
    raiz.withdraw()  # Oculta la ventana principal

    # Abre diálogos para seleccionar las versiones antigua y nueva del archivo
    ruta_version_antigua = filedialog.askopenfilename(title="Selecciona la versión antigua del archivo")
    ruta_version_nueva = filedialog.askopenfilename(title="Selecciona la versión nueva del archivo")

    # Compara las versiones seleccionadas
    Comparar_versiones(ruta_version_antigua, ruta_version_nueva)


# Punto de entrada principal del programa
if __name__ == "__main__":
    Abrir_dialogo_archivo()
