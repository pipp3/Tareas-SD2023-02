import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cargar el JSON de autos
with open('cars.json', 'r') as file:
    autos_data = json.load(file)

# Ruta para buscar un auto por ID
@app.route('/buscar_por_id/<int:auto_id>', methods=['GET'])
def buscar_por_id(auto_id):
    for auto in autos_data:
        if auto['id'] == auto_id:
            return jsonify(auto)
    return jsonify({"mensaje": "Auto no encontrado"}), 404

# Ruta para simular N búsquedas aleatorias
@app.route('/simular_busquedas/<int:num_busquedas>', methods=['GET'])
def simular_busquedas(num_busquedas):
    resultados = []
    for _ in range(num_busquedas):
        random_id = random.randint(0, 99)
        for auto in autos_data:
            if auto['id'] == random_id:
                resultados.append(auto)
                break
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
