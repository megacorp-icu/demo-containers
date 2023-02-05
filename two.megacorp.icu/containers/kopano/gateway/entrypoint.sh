#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_GATEWAY_ /etc/kopano/gateway.cfg

# Start the server!
exec /usr/sbin/kopano-gateway
