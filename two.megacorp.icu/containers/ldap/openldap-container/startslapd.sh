#!/bin/bash
set -e

mkdir -p /data/ssl

if [ ! -e /data/conf.d ]; then
  mkdir -p /data/conf.d
  mkdir -p /data/databases
  python3 /usr/local/sbin/createconfig.py
fi

if [ ! -e /data/ssl/slapd.dh.params ]; then
  openssl dhparam -out /data/ssl/slapd.dh.params 2048
fi

chown -R ldap.ldap /data
unset INITIAL_ROOTPW

echo "
# OpenLDAP pwdChecker library configuration

#useCracklib 1
minPoints ${PWCHECK_MINPOINTS}
minUpper ${PWCHECK_MINUPPER}
minLower ${PWCHECK_MINLOWER}
minDigit ${PWCHECK_MINDIGIT}
minPunct ${PWCHECK_MINPUNCT}
" > /etc/openldap/check_password.conf

urls=""
if [ ${SLAPD_LISTEN_LDAP} -eq 1 ]; then urls="$urls ldap://"; fi
if [ ${SLAPD_LISTEN_LDAPS} -eq 1 ]; then urls="$urls ldaps://"; fi
if [ ${SLAPD_LISTEN_LDAPI} -eq 1 ]; then urls="$urls ldapi://%2Fdata%2Fldapi/"; fi

exec /usr/sbin/slapd -h "${urls}" -u ldap -d${SLAPD_LOGLEVEL} -F /data/conf.d
