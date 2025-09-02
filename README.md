## Pasos

1) Crear imagen del templates-service
2) Crear imagen del file-converter-service
3) Iniciar contenedores con docker compose

## Comandos

Iniciar Contenedores(En la carpeta donde esta el docker-compose.yml): docker compose up -d

Matar los Contenedores(En la carpeta donde esta el docker-compose.yml): docker compose down

Matar los Contenederos con los volumenes(En la carpeta donde esta el docker-compose.yml): docker compose down -v

Construir una imagen(En la carpeta donde esta el Dockerfile de la imagen): docker build -t nombre_imagen:tag .

Borrar una imagen: docker image rm nombre_imagen:tag

Crear y correr un contenedor: docker run -d --name nombre_contenedor -p puerto_host:puerto_contenedor nombre_imagen:tag

Parar un Contenedor: docker container stop nombre_contenedor

Arrancar un Contenedor(Ya creado): docker container start nombre_contenedor

Borrar un Contenedor: docker container rm nombre_contenedor

