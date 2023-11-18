import csv
import re

def procesar_linea(linea):
    # Utilizar una expresión regular para dividir la línea en palabra y pares (id_doc, frecuencia)
    match = re.match(r'^([a-zA-Z]+)\s*\((.*?)\)\s*$', linea.strip())
    
    if match:
        # Extraer la palabra
        palabra = match.group(1)
        
        # Extraer la parte entre paréntesis
        contenido_par = match.group(2)
        
        # Dividir en pares (id_doc, frecuencia)
        pares = contenido_par.split(') (')
        
        for elemento in pares:
            # Dividir el par en id_doc y frecuencia
            id_doc, frecuencia = elemento.split(',')

            # Verificar si id_doc es un número
            if id_doc.isdigit():
                yield palabra, int(id_doc), int(frecuencia)
            else:
                print(f"ID_doc no es un número válido: {id_doc}")

# Ruta al archivo de texto de entrada
archivo_entrada = "part-00000.txt"

# Ruta al archivo CSV de salida
archivo_salida = "db.csv"

# Abrir el archivo CSV en modo escritura
with open(archivo_salida, 'w', newline='') as csvfile:
    # Crear un objeto escritor CSV
    csv_writer = csv.writer(csvfile)

    # Escribir encabezados al archivo CSV
    csv_writer.writerow(['Palabra', 'ID_doc', 'Frecuencia'])

    # Leer el archivo de texto línea por línea y procesar cada línea
    with open(archivo_entrada, 'r') as file:
        for linea in file:
            for palabra, id_doc, frecuencia in procesar_linea(linea):
                # Escribir los datos al archivo CSV
                csv_writer.writerow([palabra, id_doc, frecuencia])
