#!/bin/bash

trap "exit" SIGINT
trap "exit" SIGTERM

if [ -z "${PYZOR_HOMEDIR}" ]; then
  export PYZOR_HOMEDIR="/var/lib/mail/spamassassin/pyzor"
fi

SPAMASSASSIN_PYZOR_OPTIONS+=" --homedir=${PYZOR_HOMEDIR}"
export SPAMASSASSIN_PYZOR_OPTIONS

if [ -x "${MAIL_MESSAGE_SIZE_LIMIT}" ]; then
  MAIL_MESSAGE_SIZE_LIMIT=5242880
fi

/root/spamassassin-config.py

if [ "$1" == "spamd" ]; then
  sa-update
  mkdir -p "${PYZOR_HOMEDIR}"

  chown -R postfix:postfix /var/lib/mail/spamassassin/

  exec spamd -x -u postfix -g postfix --create-prefs --max-children 5 --helper-home-dir \
    --virtual-config-dir=/var/lib/mail/spamassassin/%u -x --allow-tell --syslog-socket=none \
    --socketpath=/var/spool/postfix/sockets/spamassassin.sock --socketowner=postfix --socketgroup=postfix
fi

if [ "$1" == "milter" ]; then
  rsyslogd -n&

  if [ ! -z "${MILTER_SAFE_NETWORKS}" ]; then
    SAFE_NETWORKS="-i ${MILTER_SAFE_NETWORKS}"
  fi

  exec spamass-milter -u nobody -g postfix -p /var/spool/postfix/sockets/spamassassin-milter.sock \
    ${SAFE_NETWORKS} -d misc -- -U /var/spool/postfix/sockets/spamassassin.sock --max-size=${MAIL_MESSAGE_SIZE_LIMIT}
fi

if [ "$1" == "inotify-spamlearn" ]; then
  crudini --set /etc/inotify-spamlearn.cfg paths spam_dir "${SPAMLEARN_SPAM_DIR}"
  crudini --set /etc/inotify-spamlearn.cfg paths ham_dir "${SPAMLEARN_HAM_DIR}"
  crudini --set /etc/inotify-spamlearn.cfg spam spamcmd "/usr/bin/sa-learn --spam --max-size=${MAIL_MESSAGE_SIZE_LIMIT}"
  crudini --set /etc/inotify-spamlearn.cfg spam hamcmd "/usr/bin/sa-learn --spam --max-size=${MAIL_MESSAGE_SIZE_LIMIT}"

  exec /usr/local/bin/inotify-spamlearn.py
fi

exec "$@"
