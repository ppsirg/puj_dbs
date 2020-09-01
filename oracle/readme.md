Para inicializar el motor se debe:

1. modificar el archivo init02.sql y actualizar el modelo de la BD "MER"
2. modificar el archivo init03.sql y agregar las instrucciones "INSERT" para carga de datos de prueba
3. Lanzar el contenedor con la funcionalidad docker-compose y el comando "docker-compose up --build"
4. para conectarse a oracle utilice el usuario: pujlab, clave: Pujlab123!, ip: 127.0.0.1, puerto: 1521 
5. MER: ![MER](https://github.com/ppsirg/puj_dbs/blob/master/oracle/MER-V1.jpeg?raw=true)
6. Conexion Ejemplo: ![Conexion de ejemplo](https://github.com/ppsirg/puj_dbs/blob/master/oracle/ejemploconn.png?raw=true)