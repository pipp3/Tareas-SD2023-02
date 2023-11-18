import os
import requests
import json


entradas = [
   "mazda", "nissan", "toyota", "mitsubishi", "suzuki",
    "bentley", "ferrari", "lamborghini", "lotus", "bugatti",
    "audi", "bmw", "mercedes", "honda", "ford",
    "chevrolet", "volkswagen", "porsche", "subaru", "jaguar",
    "kia", "hyundai", "volvo", "tesla", "lexus",
    "cadillac", "maserati", "Jeep", "Chrysler", "Dodge"
]
url = "https://en.wikipedia.org/w/api.php"
i = 1

for entrada in entradas:
    params = {
        'format': 'json',
        'action': 'query',
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'redirects': 1,
        'titles': entrada
    }

    req = requests.get(url, params=params).json()

    n_page = list(req['query']['pages'].keys())[0]
    texto = req['query']['pages'][n_page]['extract']
    texto = '{}<splittername>{}'.format(i, json.dumps(texto))

    if i <= 15:
        folder_path = '../carpeta1/'
    else:
        folder_path = '../carpeta2/'

    # Crea el directorio si no existe
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f'{entrada}.txt')

    with open(file_path, 'w') as f:
        f.write(texto)

    i += 1