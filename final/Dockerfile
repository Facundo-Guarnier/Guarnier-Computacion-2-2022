# FROM ubuntu:latest
FROM redis
# FROM python:3.9

#! Variables
ENV puerto 5000


#! Intalar MongoDB
RUN apt-get update 

RUN apt install -y wget
WORKDIR /home/downloads/
RUN wget https://repo.mongodb.org/apt/debian/dists/bullseye/mongodb-org/6.0/main/binary-amd64/mongodb-org-server_6.0.5_amd64.deb

RUN apt --fix-broken install
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y libcurl4
RUN dpkg -i mongodb-org-server_6.0.5_amd64.deb
RUN mkdir /home/db
# CMD mongod --dbpath /home/db


#! Intalar MongoSH
WORKDIR /home/downloads/
RUN wget https://downloads.mongodb.com/compass/mongodb-mongosh_1.8.0_amd64.deb
RUN dpkg -i mongodb-mongosh_1.8.0_amd64.deb

# CMD mongod --dbpath ~/home/db


#! Instalar herramientas del sistema
RUN apt-get install net-tools
RUN apt install -y htop
RUN apt install nano
RUN apt install -y redis-tools
RUN apt-get install -y iproute2
RUN apt-get install -y tcpdump
RUN apt-get install iputils-ping
RUN apt install -y nmap


#! Instalar python y modulos
RUN apt-get install -y python3 
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

RUN pip3 install pymongo
RUN pip3 install pickle5
RUN pip3 install motor
RUN pip3 install pandas


#! Instalar git y clonar repo
RUN apt-get install -y git
WORKDIR /home/repo_git/
RUN git clone https://github.com/Facundo-Guarnier/Computacion_2.git
WORKDIR /home/repo_git/Computacion_2/final/app/server


#! Iniciar Redis
# CMD redis-server --daemonize yes  


#! Instalar Celery 
RUN pip install celery
RUN pip install celery[redis]

# CMD celery -A celery_task worker --loglevel=INFO -c4



#! Documentar puertos que el contenedor utilizará. 
EXPOSE 6379
EXPOSE 27017
EXPOSE 5000


#! Ejecucion en paralelo de 2 o mas comandos.
CMD mongod --dbpath /home/db --fork --logpath /var/log/mongodb.log \
    && redis-server --daemonize yes \
    && celery -A celery_task worker --loglevel=INFO --detach\
    && tail -f /dev/null  
#! Mongo: El --dbpath indica la ruta de la DB. El --fork indica que se debe ejecutar en segundo plano esto obliga usar --logpath para guardar el regustro en un archivo.
#! Redis: --daemonize indica que se ejecute en segundo plano. testiar con redis-cli ping.
#! Celery: --detach indica que se ejecute en segundo plano.
#! tail -f /dev/null Hace que el contenedor se quede leyendo un documento, esto evita que se cierre el contenedo apenas termine de ejecutar los comandos anteriores.

#* Comandos de Docker
#! Crear una imagen a travez del dockerfile.
# docker build -t nombre_new_imagen .

#! Crear un contenedor dese una imagen
# docker run -it -e puerto=5000 my_image
# docker run -it -e puerto=5000 -p 5000:5000 imagen_compu2

#! iniciar un contenedor
# docker start nombre_contenedor

#! Abrir una terminal en un contenedor que está corriendo.
# docker exec -it nombre_contenedor bash

#! Ver IP de un contenedor.
# docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nombre_contenedor