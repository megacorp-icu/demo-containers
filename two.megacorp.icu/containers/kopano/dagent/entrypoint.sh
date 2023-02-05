#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_DAGENT_ /etc/kopano/dagent.cfg
/root/configfile.sh KC_ARCHIVER_ /etc/kopano/archiver.cfg

# Start the server!
exec /usr/sbin/kopano-dagent -l
