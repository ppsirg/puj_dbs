# Funcionamiento de la aplicacion


1. Ejecutar el comando "docker-compose up --build -d", este es el encargado de inicializar el motor oracle y la aplicacion en python 
2. Para acceder a la aplicacuin ingrese a la direccion http://{host}:80 y haces uso de las siguientes API's:
    2.1 http://{host}:80/login/{user_id}
    2.2 http://{host}:80/followers/differential/{user_a_email}/{user_b_email}
    2.3 http://{host}:80//user_by_email/{email}
    2.4 http://{host}:80//list_recent_users_tweet/
    2.5 http://{host}:80//city_rank/
    2.6 http://{host}:80//followers_tree/{root_email}


# Informacion detallada:

1. Archivo database-environment/init02.sql contiene el modelo de la BD "MER"
2. Arcivo database-environment/init03.sql contiene las instrucciones "INSERT" para carga de datos de prueba
3. Lanzar el contenedor con la funcionalidad docker-compose y el comando "docker-compose up --build -d", inicializa el motor y la app
4. para conectarse a oracle utilice el usuario: pujlab, clave: Pujlab123!, ip: 127.0.0.1, puerto: 1521 
5. MER: ![MER](https://github.com/ppsirg/puj_dbs/blob/master/oracle/database_design/MER-V1.jpeg?raw=true)
6. Conexion Ejemplo: ![Conexion de ejemplo](https://github.com/ppsirg/puj_dbs/blob/master/oracle/database_design/ejemploconn.png?raw=true) 