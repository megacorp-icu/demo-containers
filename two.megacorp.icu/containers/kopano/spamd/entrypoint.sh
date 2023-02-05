#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_SPAMD_ /etc/kopano/spamd.cfg

mkdir -p ${KC_SPAMD_spam_dir} ${KC_SPAMD_ham_dir} $(dirname ${KC_SPAMD_spam_db})
chown -R ${KC_SPAMD_run_as_user}:${KC_SPAMD_run_as_group} $(dirname ${KC_SPAMD_spam_db}) $(dirname ${KC_SPAMD_spam_dir}) $(dirname ${KC_SPAMD_ham_dir})

# Start the server!
exec /usr/sbin/kopano-spamd
