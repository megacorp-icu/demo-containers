#!/bin/bash

mkdir -p /run/saslauthd
chown -R postfix:postfix /run/saslauthd

exec /usr/sbin/saslauthd -d 1 -c -m /run/saslauthd -a rimap -O "${SASLAUTHD_IMAP_SERVER}"
