#!/bin/bash

python3 /root/config.py
mkdir -p /etc/opendkim/keys
touch /etc/opendkim/TrustedHosts
touch /etc/opendkim/KeyTable
touch /etc/opendkim/SigningTable

chown -R postfix:postfix /etc/opendkim*
chown postfix:postfix /var/spool/postfix/sockets

rsyslogd -n&
exec opendkim -l -x /etc/opendkim.conf
