# Tarea 1 Sistemas Distribuidos

Para ejecutar la API se debe usar previamente `pip install Flask`

Para ejecutar el contenedor de memcached `docker run -d --name memcached-container --network cache_memcach_cache_network -p 11211:11211 memcached:alpine -m 128`

Recordar que el sistema de cache casero no se puede usar al mismo tiempo que el sistema con memcached ya que los dos usan el mismo nombre de contenedor. Porfavor probar un sistema, luego cerrar la ejecucuion con `ctrl+c` y finalemente ejecutar `docker compose down`.

En el siguiente [video](https://youtu.be/oahwxIynaxM) se puede ver el funcionamiento y la explicacion de los sistemas que se pidieron.
