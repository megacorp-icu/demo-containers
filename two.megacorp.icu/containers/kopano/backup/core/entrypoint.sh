#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_SERVER_ /etc/kopano/server.cfg

echo -n "CORE: Waiting for database: "
while ! /usr/bin/mysql -u "${KC_SERVER_mysql_user}" --password="${KC_SERVER_mysql_password}" --host="${KC_SERVER_mysql_host}" --database="${KC_SERVER_mysql_database}" -e "SHOW GRANTS" &> /dev/null; do
	echo -n "."
	sleep 1s
done

echo
echo "CORE: Connected!"

# These are noops when it has already been done.
kopano-dbadm k-1216
kopano-dbadm usmp

# Start the server!
/usr/sbin/kopano-server -F
