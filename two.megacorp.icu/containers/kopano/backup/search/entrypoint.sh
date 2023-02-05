#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_SEARCH_ /etc/kopano/search.cfg

# Start the server!
/usr/sbin/kopano-server -F
