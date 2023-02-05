#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_ARCHIVER_ /etc/kopano/archiver.cfg

while /bin/true; do
  /usr/sbin/kopano-archiver -A --auto-attach
  sleep 30m
done
