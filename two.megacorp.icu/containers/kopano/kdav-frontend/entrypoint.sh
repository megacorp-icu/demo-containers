#!/bin/bash

chown -R kopano.kopano /var/lib/kopano/kdav

exec nginx -g 'daemon off;'
