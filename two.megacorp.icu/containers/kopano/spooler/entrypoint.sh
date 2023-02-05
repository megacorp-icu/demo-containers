#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_SPOOLER_ /etc/kopano/spooler.cfg

# Start the server!
exec /usr/sbin/kopano-spooler
