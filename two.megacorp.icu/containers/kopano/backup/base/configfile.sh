#!/bin/bash
set -e

if [ -z "${1}" ]; then
	echo "Need a environment variable prefix"
	exit 1
fi

if [ -z "${2}" ]; then
	echo "Need a config file name"
	exit 1
fi

for variable in $(awk "BEGIN {for (k in ENVIRON) { if(k ~ /^${1}/) print k }}"); do
	ini_name=$(echo $variable | sed -e "s/${1}//")
	crudini --set "${2}" "" "${ini_name}" "${!variable}"
done
