#!/bin/bash
set -e

if [ -z "${1}" ]; then
	echo "Need a environment variable prefix"
	exit 1
fi

for variable in $(awk "BEGIN {for (k in ENVIRON) { if(k ~ /^${1}/) print k }}"); do
	var_name=$(echo $variable | sed -e "s/${1}//")
	sed -ie "s|define(\"${var_name}\", .*);|define(\"${var_name}\", ${!variable});|" /etc/kopano/webapp/config.php
done
