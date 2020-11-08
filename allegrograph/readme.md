# Funcionamiento de la aplicacion

1. MER: ![MER](https://github.com/ppsirg/puj_dbs/blob/master/allegrograph/RDF_PUJ_Taller.png?raw=true)
2. Ejecutar el comando 
´´´
docker run -it --rm \
         --shm-size 1g \
         -v agdata:/agraph/data \
         -v agconfig:/agraph/etc \
         -e AGRAPH_SUPER_USER=admin \
         -e AGRAPH_SUPER_PASSWORD=pass \
         -p 10000-10035:10000-10035 \
         --name agraph-instance-1 \
         franzinc/agraph:v7.0.0
´´´
3. Ingresar a la consola web en la direccion http://localhost:10035 con el usuario admin y la clave pass
4. Crear un repositorio llamado pujlab-rdf
5. Ingresar al repositorio creado y cargar el Archivo data-taller.txt por la funcionalidad de importar datos
