import requests
import csv

def obtener_url_pagina_wikipedia(titulo, idioma='es'):
    base_url = f'https://{idioma}.wikipedia.org/w/api.php'
    parametros = {
        'action': 'query',
        'titles': titulo,
        'format': 'json',
        'prop': 'info',
        'inprop': 'url'
    }

    respuesta = requests.get(base_url, params=parametros)
    datos = respuesta.json()

    # Obtener la URL de la primera página en la respuesta
    pagina = next(iter(datos['query']['pages'].values()))
    if 'fullurl' in pagina:
        return pagina['fullurl']
    else:
        print(f"La página de Wikipedia '{titulo}' no existe.")
        return None

def guardar_en_csv(urls, archivo_csv):
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Documento", "URL"])  # Encabezados del CSV

        for documento, url in enumerate(urls.values(), start=1):
            writer.writerow([documento, url])

# Lista de páginas de Wikipedia
paginas_wikipedia = ["mazda", "nissan", "toyota", "mitsubishi", "suzuki",
    "bentley", "ferrari", "lamborghini", "lotus", "bugatti",
    "audi", "bmw", "mercedes", "honda", "ford",
    "chevrolet", "volkswagen", "porsche", "subaru", "jaguar",
    "kia", "hyundai", "volvo", "tesla", "lexus",
    "cadillac", "maserati", "Jeep", "Chrysler", "Dodge"]

# Obtener las URLs
urls_wikipedia = {}
for pagina in paginas_wikipedia:
    url = obtener_url_pagina_wikipedia(pagina)
    if url:
        urls_wikipedia[pagina] = url

# Guardar en un archivo CSV
archivo_csv = "urls.csv"
guardar_en_csv(urls_wikipedia, archivo_csv)

print(f"Las URLs se han guardado en el archivo CSV: {archivo_csv}")
