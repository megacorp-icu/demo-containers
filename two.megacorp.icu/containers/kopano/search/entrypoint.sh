#!/bin/bash

# Generate our configuration files
/root/configfile.sh KC_SEARCH_ /etc/kopano/search.cfg

chown ${KC_SEARCH_run_as_user}:${KC_SEARCH_run_as_group} ${KC_SEARCH_index_path}

# Start the server!
exec /usr/sbin/kopano-search
