# Kafka en NodeJs y API de ventas basica

### Ejecucion
Usar `docker compose up` para levantar la API, KAFKA , ZOOKEEPER y POSTGRESQL.
### Configuracion
Para conectarse a la Base de datos:
1. Ingresar a [PGADMIN](http://localhost/browser/)
2. Credenciales: email: admin@admin.com && pass: admin
3. Para ingresar al servidor que contiene la BDD usar: pass: root
Crear tablas:
1. users: Crear campos id(Pk,auto incrementable),nombre, email,rut.
2. carrito: Crear campos: id(Pk,auto incrementable),stock,usuario_id(fk).
3. ventas: Crear campos: id(Pk,auto incrementable), ganancias,usuario_id(fk),semana.

### Demo
Usando este link puedes ver como se usa/funciona el sistema [Video](https://youtu.be/5x0ACp96o3w).
