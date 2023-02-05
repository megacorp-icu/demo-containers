#!/bin/bash

chown kopano.kopano /var/lib/z-push

exec nginx -g 'daemon off;'
