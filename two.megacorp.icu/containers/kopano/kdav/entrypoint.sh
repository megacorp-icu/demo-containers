#!/bin/bash

/root/php_configfile.sh KC_KDAV_ /usr/share/kdav/config.php

chown -R kopano.kopano /var/lib/kopano/kdav

exec php-fpm7.4 -RF
