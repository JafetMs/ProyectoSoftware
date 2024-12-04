import tkinter as tk 
from tkinter import filedialog
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

        if '#' in linea:  # Verifica si hay un comentario
            indice_comentario = linea.index('#')
        
            # Verificar si el '#' está dentro de comillas simples o dobles
            dentro_simple = False
            dentro_doble = False

            for j, char in enumerate(linea):

                if char == "'" and (j == 0 or linea[j - 1] != '\\'):  # Cambiar estado para comillas simples
                    dentro_simple = not dentro_simple

                elif char == '"' and (j == 0 or linea[j - 1] != '\\'):  # Cambiar estado para comillas dobles
                    dentro_doble = not dentro_doble

                if j == indice_comentario and (dentro_simple or dentro_doble):
                    break  # Si el '#' está dentro de comillas, ignorar la línea

            else:
                # Procesar solo si el '#' no está dentro de comillas
                partes = linea.split('#', 1)  # Divide la línea en dos partes en el símbolo #
                despues_del_hash = partes[1]  # Obtiene el texto después del #

                # Verificar que hay exactamente 1 espacio después del #
                if not re.match(r'^ [^\s]', despues_del_hash):
                    raise Exception(f"Línea {i+1}: Debe haber exactamente un espacio después de '#'")
            
                comentario = despues_del_hash.strip()  # Elimina espacios alrededor del comentario
            
                # Verificar que el comentario empieza con mayúscula y no está vacío
                if not comentario or comentario[0].islower():
                    raise Exception(f"Línea {i+1}: Comentario no empieza con mayúscula o está vacío")

        # Verificar las comas
        if ',' in linea:
            dentro_comillas = False  # Bandera para saber si estamos dentro de comillas

            for j, char in enumerate(linea):

                if char in "'\"":  # Cuando encontramos una comilla

                    # Cambiar el estado de la bandera (si estamos dentro de comillas o no)
                    if j == 0 or linea[j-1] != '\\':  # Evitar los escapes de comillas
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
        
        linea = linea.strip()  # Elimina espacios en blanco al inicio y al final
    
        # Verificar si es una declaración de clase
        if linea.startswith("class "):  # Identifica si es una clase
            raise Exception(f"Línea {i+1}: El uso de class, es solo para programación orientada a objetos")
    
        # Verificar si es una declaración de función
        elif linea.startswith("def "):  # Identifica si es una función
            nombre_funcion = linea.split()[1].split('(')[0]  # Obtiene el nombre de la función

            if not nombre_funcion[0].isupper():
                raise Exception(f"Línea {i+1}: El nombre de la función '{nombre_funcion}' no comienza con mayuscula") 
    
    print("El archivo cumple con los estándares.")


def Contar_lineas_logicas(file_path):
    # Inicialización de contador
    lineas_logicas = 0

    # Palabras clave consideradas como líneas lógicas
    palabras_clave = {"if", "for", "while", "def", "try", "with"}

    try:

        # Abrir y leer el archivo línea por línea
        with open(file_path, 'r') as archivo:

            for linea in archivo:
                # Eliminar espacios en blanco y comentarios
                linea = linea.strip()

                if linea.startswith("#") or len(linea) == 0:
                    continue
                
                # Verificar si la línea comienza con alguna palabra clave lógica
                linea_logica = False

                for palabra in palabras_clave:

                    if linea.startswith(palabra):
                        linea_logica = True
                        break
                
                # Incrementar el contador si es una línea lógica
                if linea_logica:
                    lineas_logicas += 1

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    
    return lineas_logicas


def Contar_lineas_fisicas(file_path):
    # Inicialización de contadores
    lineas_fisicas = 0
    try:

        # Abre el archivo en modo de solo lectura
        with open(file_path, 'r') as archivo:

            for linea in archivo:  # Itera por cada línea en el archivo
                # Excluye líneas vacías y comentarios
                linea = linea.strip()

                if linea.startswith("#") or len(linea) == 0:
                    continue
                lineas_fisicas += 1  # Incrementa el contador de líneas físicas por cada línea leída

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")        
    
    # Devuelve el contador
    return  lineas_fisicas


# Bloque principal: Punto de entrada del programa
if __name__ == "__main__":
    # Crea una ventana oculta para abrir el cuadro de diálogo de selección de archivos
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    # Abre una ventana para seleccionar un archivo
    archivo = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Archivos de Python", "*.py"), ("Todos los archivos", "*.*")])

    if archivo:  # Verifica si el usuario seleccionó un archivo
        
        try:
            # Verificar si el archvio cumple con los estandares de codificación
            errores = Verificar_estandares_archivo(archivo)
            # Llama a las funciones para contar las líneas
            loc_fisicas = Contar_lineas_fisicas(archivo)
            loc_logicas = Contar_lineas_logicas(archivo)
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