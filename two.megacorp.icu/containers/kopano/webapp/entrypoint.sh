#!/bin/bash

/root/php_configfile.sh KC_WEBAPP_ /etc/kopano/webapp/config.php

chmod 777 /var/lib/kopano-webapp/tmp

exec php-fpm7.4 -RF
