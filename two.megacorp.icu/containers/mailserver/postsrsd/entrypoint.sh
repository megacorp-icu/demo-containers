#!/bin/bash

echo ${POSTSRSD_SECRET} > /etc/postsrsd.secret
chown -R postfix:postfix /etc/postsrsd.secret

exec /usr/sbin/postsrsd -f 10001 -r 10002 -d "${POSTSRSD_DOMAIN}" -s /etc/postsrsd.secret -a = -n 4 -N 4 -u postfix -l 0.0.0.0 "-X${POSTSRSD_EXCLUDE_DOMAINS}"
