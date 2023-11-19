## *Paso 1 MapReduce y Hadoop (contar palabras)*

Primero que todo se debe levantar el contenedor ``` docker compose up ``` .
Otro detalle de suma relevancia, si es que están en windows, deben de cambiar el interprete de crlf a lf. Los archivos que se deben cambiar son mapper.py, reducer.py y docker-entrypoint.sh .

Posterior a lo anterior deben de configurar un usuario que administrará todos los comandos y por ello es necesario que sigan las siguientes instrucciones y/o comandos:

**[0]** Se accede al contenedor que contiene el servicio de hadoop:
```sh
docker exec -it hadoop bash
```
**[1]** Se creará un respectivo directorio para gestionar las acciones del usuario hduser (es imporatnte que tenga este nombre para todos los comandos)\
Creación de carpeta para usuario:
```sh
hdfs dfs -mkdir /user
```
Creación de usuario en el directorio:
```sh
hdfs dfs -mkdir /user/hduser
```
Creación de directorio para el procesamiento archivos y/o textos:
```sh
hdfs dfs -mkdir input
```
**[2]** Damos los permisos tantos del usuario y del directorio
```sh
sudo chown -R hduser .
```
**[3]** Cargamos los txt extraidos de wikipedia a hadoop mediante los siguientes comandos, primero accedemos a la carpeta donde estan alojados y se ejecuta hdfs.
```sh
cd examples/
hdfs dfs -put carpeta1/*.txt input
hdfs dfs -put carpeta2/*.txt input
```
Se puede validar que efectivamente se hayan procesado dichos archivos contenidos en los directorios con el siguiente comando:
```sh
hdfs dfs -ls input
```

**[4]** Se ejecutan  mapper y reducer par el conteo de palabras de los archivos.
```sh
mapred streaming -files mapper.py,reducer.py -input /user/hduser/input/*.txt -output hduser/outhadoop/ -mapper ./mapper.py -reducer ./reducer.py
```
Luego el archivo lo exportamos al entorno local en linux dentro del contenedor y en este caso dentro del directorio examples. Allí quedará una carpeta de nombre output con un contador de palabras por archivo y en este caso sería uno general para todos los datos volcados tanto en la *carpeta1* como en la *carpeta2*. 

Es aquí donde entra el uso del volumen para así extraer de forma efectiva el archivo ya procesado, por hadoop.
```sh
hdfs dfs -get /user/hduser/hduser/outhadoop/ /home/hduser/examples
```
