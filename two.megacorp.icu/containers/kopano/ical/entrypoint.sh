#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_ICAL_ /etc/kopano/ical.cfg

# Start the server!
exec /usr/sbin/kopano-ical
