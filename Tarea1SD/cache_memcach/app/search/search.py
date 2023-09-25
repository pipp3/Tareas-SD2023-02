import time
import numpy as np
import memcache  # Importa la biblioteca python-memcached
from find_car_by_id import find_car_by_id

class CacheClient:
    def __init__(self, host="localhost", port=11211):
        self.mc = memcache.Client([f"{host}:{port}"])

    def get(self, key, simulated=False):
        start_time = time.time()

        value = self.mc.get(key)

        if value:
            elapsed_time = time.time() - start_time
            print(f"Tiempo transcurrido (caché): {elapsed_time:.5f} segundos")
            return value.decode()
        else:
            delay = np.random.normal(2, 0.5)
            print(f"Clave no encontrada en caché. Esperando {delay:.5f} segundos...")

            value = find_car_by_id(int(key))
            value = str(value)
            if value:
                print("Clave encontrada en JSON. Agregando al caché...")
                self.mc.set(key, value)
                
                elapsed_time = time.time() - start_time
                if simulated:
                    elapsed_time += delay
                print(f"Tiempo transcurrido (JSON + retraso): {elapsed_time:.5f} segundos")
                
                return value
            else:
                elapsed_time = time.time() - start_time
                print(f"Tiempo transcurrido: {elapsed_time:.5f} segundos")
                print("Clave no encontrada.")
                return None
            
    def simulate_searches(self, n_searches=100):
        keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_searches)]

        tiempo_sin_cache = 0
        tiempo_con_cache = 0
        evitadas_consultas_json = 0

        count = 0
        for key in keys_to_search:
            count += 1
            print("\033[H\033[J")
            print(f"Búsqueda: {count}/{n_searches}")
            start_time = time.time()
            tiempo_sin_cache += 3 + 0.001  # Tiempo estimado de búsqueda en JSON
            self.get(key)
            elapsed_time = time.time() - start_time
            tiempo_con_cache += elapsed_time

            if elapsed_time < 1:
                evitadas_consultas_json += 1

        tiempo_guardado = tiempo_sin_cache - tiempo_con_cache
        print(f"\nTiempo ahorrado gracias al caché: {tiempo_guardado:.2f} segundos")
        print(f"Número de veces que se evitó la búsqueda en JSON: {evitadas_consultas_json}")
        print(f"Latencia de búsqueda: {elapsed_time:.5f} segundos")

if __name__ == '__main__':
    cliente = CacheClient()

    while True:
        print("\nElija una operación:")
        print("1. Obtener")
        print("2. Simular Búsquedas")
        print("3. Salir")

        elección = input("Ingrese su elección: ")

        if elección == "1":
            clave = input("Ingrese la clave: ")
            valor = cliente.get(clave)
            if valor is not None:
                print(f"Valor: {valor}")
        elif elección == "2":
            n_busquedas = int(input("Ingrese el número de búsquedas que desea simular: "))
            cliente.simulate_searches(n_busquedas)
        elif elección == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Elección no válida. Intente de nuevo.")
