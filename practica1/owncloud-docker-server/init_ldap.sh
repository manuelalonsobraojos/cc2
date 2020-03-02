#!/bin/bash
# Automatizar el proceso de levantamiento y configuración

#docker-compose up --scale owncloud=2 -d

#docker exec ownclouddockerserver_owncloud_1 occ app:enable user_ldap &> /dev/null

#while [ $? -ne 0 ]
#do
	#sleep 1
	#docker exec ownclouddockerserver_owncloud_1 occ app:enable user_ldap &> /dev/null
#done

 

# Poner contraseña como variable de entorno

# Configura OwnCloud para usar el servidor de LDAP 

docker exec ownclouddockerserver_owncloud_1 occ app:enable user_ldap \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_agent_password --value=cGFzc3dvcmQ= \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_base --value=dc=openstack,dc=org \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_base_groups --value=dc=openstack,dc=org \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_base_users --value=dc=openstack,dc=org \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_configuration_active --value=1 \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_display_name --value=cn \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_dn --value=cn=admin,dc=openstack,dc=org \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_host --value=ownclouddockerserver_ldap_1 \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_login_filter --value='(&(|(objectclass=inetOrgPerson))(uid=%uid))' \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_port --value=389 \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_userfilter_objectclass --value=inetOrgPerson \

docker exec ownclouddockerserver_owncloud_1 occ config:app:set user_ldap s01ldap_userlist_filter  --value='(|(objectclass=inetOrgPerson))'
