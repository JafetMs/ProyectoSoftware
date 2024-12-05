import tkinter as tk   
from tkinter import filedialog 
from tabulate import tabulate
import re


def Verificar_estandares_archivo(archivo):
    
    with open(archivo, 'r') as f:
        lineas = f.readlines()

    errores = []
    estructuras_control = ['if', 'elif', 'else', 'for', 'while', 'def', 'try', 'except']

    for i, linea in enumerate(lineas):
        
        # Verificar longitud de línea
        if len(linea) > 79:
            errores.append(f"Línea {i+1}: Excede los 80 caracteres")

        # Verifica si hay un comentario
        if '#' in linea:  
            indice_comentario = linea.index('#')
        
            # Verificar si el '#' está dentro de comillas simples o dobles
            dentro_simple = False
            dentro_doble = False

            for j, char in enumerate(linea):

                # Cambiar estado para comillas simples
                if char == "'" and (j == 0 or linea[j - 1] != '\\'):  
                    dentro_simple = not dentro_simple

                # Cambiar estado para comillas dobles
                elif char == '"' and (j == 0 or linea[j - 1] != '\\'):  
                    dentro_doble = not dentro_doble

                # Si el '#' está dentro de comillas, ignorar la línea
                if j == indice_comentario and (dentro_simple or dentro_doble):
                    break  
            
            # Procesar solo si el '#' no está dentro de comillas
            else:
                # Divide la línea en dos partes en el símbolo #
                partes = linea.split('#', 1) 
                # Obtiene el texto después del # 
                despues_del_hash = partes[1]  

                # Verificar que hay exactamente 1 espacio después del #
                if not re.match(r'^ [^\s]', despues_del_hash):
                    raise Exception(f"Línea {i+1}: Debe haber exactamente un espacio después de '#'")
            
                # Elimina espacios alrededor del comentario
                comentario = despues_del_hash.strip()  
            
                # Verificar que el comentario empieza con mayúscula y no está vacío
                if not comentario or comentario[0].islower():
                    raise Exception(f"Línea {i+1}: Comentario no empieza con mayúscula o está vacío")

        # Verificar las comas
        if ',' in linea:
             # Bandera para saber si estamos dentro de comillas
            dentro_comillas = False 

            for j, char in enumerate(linea):

                # Cuando encontramos una comilla
                if char in "'\"":  

                    # Cambiar el estado de la bandera (si estamos dentro de comillas o no)
                    # Evitar los escapes de comillas
                    if j == 0 or linea[j-1] != '\\': 
                        dentro_comillas = not dentro_comillas

                # Si no estamos dentro de comillas, verificar las comas
                if not dentro_comillas and char == ',':

                    # Verificar que no haya un espacio antes de la coma
                    if j > 0 and linea[j-1] == ' ':
                        raise Exception(f"Línea {i+1}: Hay un espacio antes de la coma")

                    # Verificar que haya un espacio después de la coma
                    if j+1 < len(linea) and linea[j+1] != ' ':
                        raise Exception(f"Línea {i+1}: Falta espacio después de la coma")

        # Verificar indentación
        if linea.startswith(' ') and (len(linea) - len(linea.lstrip(' '))) % 4 != 0:
            raise Exception(f"Línea {i+1}: Indentación incorrecta, debe ser múltiplo de 4 espacios")

        if linea.startswith('"""'):
            raise Exception(f"Línea {i+1}: Comentario en bloque no permitido")
        
        # Verificar identificadores
        if re.match(r'^\s*\w+\s*=\s*', linea):
            identificador = linea.split('=')[0].strip()

            if not identificador.islower():
                raise Exception(f"Línea {i+1}: Identificador no está en minúsculas")

        # Verificar que no haya más de una estructura de control en una sola línea
        conteo_estructuras = 0
        for estructura in estructuras_control:

            if linea.lstrip().startswith(estructura):
                conteo_estructuras += 1

        if conteo_estructuras > 1:
            raise Exception(f"Línea {i+1}: Más de una estructura de control en la misma línea")
        
        # Elimina espacios en blanco al inicio y al final
        linea = linea.strip()  
    
        # Verificar si es una declaración de clase
        if linea.startswith("class "): 
            raise Exception(f"Línea {i+1}: El uso de class, es solo para programación orientada a objetos")
    
        # Verificar si es una declaración de función
        elif linea.startswith("def "): 
            nombre_funcion = linea.split()[1].split('(')[0]

            if not nombre_funcion[0].isupper():
                raise Exception(f"Línea {i+1}: El nombre de la función '{nombre_funcion}' no comienza con mayuscula") 
    
    print("El archivo cumple con los estándares.")


# Función para leer el código desde un archivo y dividirlo en funciones y bloque principal
def Leer_codigo(filename):
    with open(filename, 'r') as file:

        # Lee todas las líneas del archivo
        lines = file.readlines()  

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

    for line in lines:
        # Elimina espacios en blanco al inicio y al final de la línea
        stripped_line = line.strip()  

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
            funcion_actual.append(line)

        elif dentro_de_main:
            bloque_principal.append(line)

    # Si queda alguna función por guardar, la añade
    if funcion_actual:  
        funciones.append((nombre_funcion_actual, funcion_actual))

    return funciones, bloque_principal, lines


# Función para contar líneas físicas (líneas no vacías ni comentarios)
def Contar_lineas_fisicas(codigo):
    lineas_validas = []

    for linea in codigo:
        linea_strip = linea.strip()

        # Ignora comentarios y líneas vacías
        if linea_strip and not linea_strip.startswith("#"):  
            lineas_validas.append(linea_strip)

    return len(lineas_validas)

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
    lineas_fisicas_totales = Contar_lineas_fisicas(codigo)
    lineas_logicas_totales = Contar_lineas_logicas(codigo)

    print("\nTotales del código completo:")
    print(f"Líneas físicas: {lineas_fisicas_totales}")
    print(f"Líneas lógicas: {lineas_logicas_totales}")


# Bloque principal: Punto de entrada del programa
if __name__ == "__main__":
    # Crea una ventana oculta para abrir el cuadro de diálogo de selección de archivos
    root = tk.Tk()
    # Oculta la ventana principal
    root.withdraw()  
    # Abre un cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")])
    
    # Verifica si el usuario seleccionó un archivo
    if archivo:  

        try:
            # Lee el archivo y procesa el contenido
            Verificar_estandares_archivo(archivo)
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
