#!/bin/bash

echo -n "CORE: Waiting for database: "
while ! /usr/bin/mysql -u "${KC_SERVER_mysql_user}" --password="${KC_SERVER_mysql_password}" --host="${KC_SERVER_mysql_host}" --database="${KC_SERVER_mysql_database}" -e "SHOW GRANTS" &> /dev/null; do
	echo -n "."
	sleep 1s
done

echo
echo "CORE: Connected!"

chown ${KC_SERVER_run_as_user}:${KC_SERVER_run_as_group} ${KC_SERVER_attachment_path}

mkdir -p /var/run/kopano
chown ${KC_SERVER_run_as_user}:${KC_SERVER_run_as_group} /var/run/kopano

# Generate our configuration files
/root/configfile.sh KC_SERVER_ /etc/kopano/server.cfg
/root/configfile.sh KC_LDAP_ /etc/kopano/ldap.cfg
/root/configfile.sh KC_ARCHIVER_ /etc/kopano/archiver.cfg

# These are noops when it has already been done.
kopano-dbadm k-1216
kopano-dbadm usmp

# Start the server!
exec /usr/sbin/kopano-server -F
