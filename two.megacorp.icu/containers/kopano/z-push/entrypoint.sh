#!/bin/bash

/root/php_configfile.sh Z_PUSH_COMMON_ /etc/z-push/z-push.conf.php
/root/php_configfile.sh Z_PUSH_KOPANO_ /etc/z-push/kopano.conf.php
/root/php_configfile.sh Z_PUSH_AUTODISCOVER_ /etc/z-push/autodiscover.conf.php

chown -R kopano.kopano /var/log/z-push

exec php-fpm7.4 -RF
