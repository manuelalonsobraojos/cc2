# Práctica 1: Servicio Cloud de almancenamiento con OwnCloud

Para la creación de la arquitectura propuesta, será necesario la creación de un archivo docker-compose en el que se le especificaran la configuración de cada uno de los servicios.

El archivo docker-compose con la configuración para la creación del servicio de owncloud, ha sido cogido del siguiente [repositorio](https://raw.githubusercontent.com/owncloud/docs/master/modules/admin_manual/examples/installation/docker/docker-compose.yml). 
A continuación, en el archivo  [docker-compose.yml](https://github.com/manuelalonsobraojos/cc2/blob/master/practica1/owncloud-docker-server/docker-compose.yml) creado, se añaden los demás servicios: MariaDB, nginx y ldap, todos ellos dependientes del servicio owncloud.

Para el correcto funcionamiento del servicio de nginx, será necesario cambiar la coniguración que viene por defecto, por lo que ha sido necesario la creación de un archivo de configuración, el cual podemos ver en el siguiente enlace, [nginx.conf](https://github.com/manuelalonsobraojos/cc2/blob/master/practica1/owncloud-docker-server/nginx_conf/nginx.conf).
```
worker_processes  8;
events {
    worker_connections  1024;
}
http {
    #include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    upstream owncloud {
 	server ownclouddockerserver_owncloud_1:8080;
	 server ownclouddockerserver_owncloud_2:8080;
    }
    server {
        listen       80;
        location / {
            proxy_pass http://owncloud;
            } # end location
        } # end server
    } # end http
```
Como se puede visualizar en la coniguración, se le indica el host y el puerto de cadad servidor de owncloud creado, y en los que nginx se encargará de enrutar y balancear la carga.

Una vez creado el archivo docker-compose.yml, levantamos los servicios ejecutando el siguiente comando:
 ```
 sudo docker-compose up -d --scale owncloud=2
 ```
 Como se puede ver en el comando anterior, se le especifica la creación de dos servicios de owncloud.
 
 Una vez desplegado los servicios, es necesario la habilitación de ldap en nuestro servicio de owncloud. Para ello se ha creado un script el cual podemos ver en el siguiente enlace, [init_ldap.sh](https://github.com/manuelalonsobraojos/cc2/blob/master/practica1/owncloud-docker-server/init_ldap.sh).
 
 Una vez habilitado se procede a configurar un usuario en ldap, para ello es necesario ejecutar el siguiente comando:
 ```
 sudo docker exec -it <id-servicio-ldap /bin/sh
 ```
 Una vez ejeucta se abrirá una consola de comandos de ldap, y aquí con el siguiente comando se configura el usuario:
 ```
 ldappasswd -s Admin123 -W -D "cn=admin,dc=openstack,dc=org" -x "cn=Larry Cai,ou=Users,dc=openstack,dc=org"
 ``` 




