#!/bin/bash

export POSTFIX_MAIN_message_size_limit=${MAIL_MESSAGE_SIZE_LIMIT}
export POSTFIX_MAIN_myhostname=${MAIL_HOSTNAME}

python3 /root/config.py

chown -R postfix /certificates

exec postfix start-fg
