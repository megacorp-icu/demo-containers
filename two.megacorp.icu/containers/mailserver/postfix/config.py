#!/usr/bin/env python3

import os
import re
from inspect import cleandoc
from subprocess import run, PIPE
from pathlib import Path

domains = {}
relay_domains = []
relay_recipient_maps = []
sender_login_maps = []
relay_transport = []
recipient_bcc = []
alias = []
blackholes = []

regex = re.compile('MAIL_DOMAIN_([0-9]+)_?(.*)')
for key in os.environ.keys():
    match = regex.match(key)
    if match:
        i = match[1]
        if not i in domains: domains[i] = {}

        if not match[2]:
            domains[i]['name'] = os.environ[key]
        else:
            domains[i][match[2]] = os.environ[key]

for key, domain in domains.items():
    relay_domains.append(domain["name"])

    try:
        relay_transport.append(f"{domain['name']} {domain['TRANSPORT']}")
    except KeyError:
        pass

    try:
        filename = f"/etc/postfix/recpient-map-{domain['name']}.cf"
        recipient_map = cleandoc(f"""
        server_host = {domain["LDAP_HOST"]}
        bind_dn = {domain["LDAP_BIND_DN"]}
        bind_pw = {domain["LDAP_BIND_PASSWORD"]}
        search_base = {domain["LDAP_SEARCH_BASE"]}
        version = {domain["LDAP_VERSION"]}
        scope = {domain["LDAP_SCOPE"]}
        query_filter = {domain["LDAP_ADDRESS_FILTER"]}
        result_attribute = {domain["LDAP_ADDRESS_RESULT"]}
        domain = {domain["name"]}
        """)
        relay_recipient_maps.append(f"ldap:{filename}")

        with open(filename, "w") as f:
            f.write(recipient_map)
            f.write("\n")
    except KeyError:
        pass

    try:
        filename = f"/etc/postfix/sender-map-{domain['name']}.cf"
        sender_map = cleandoc(f"""
        server_host = {domain["LDAP_HOST"]}
        bind_dn = {domain["LDAP_BIND_DN"]}
        bind_pw = {domain["LDAP_BIND_PASSWORD"]}
        search_base = {domain["LDAP_SEARCH_BASE"]}
        version = {domain["LDAP_VERSION"]}
        scope = {domain["LDAP_SCOPE"]}
        query_filter = {domain["LDAP_ADDRESS_FILTER"]}
        result_attribute = {domain["LDAP_ADDRESS_RESULT"]}
        domain = {domain["name"]}
        """)
        sender_login_maps.append(f"ldap:{filename}")

        with open(filename, "w") as f:
            f.write(sender_map)
            f.write("\n")
    except KeyError:
        pass

    try:
        for hole in filter(None, domain["BLACKHOLE"].split(",")):
            blackholes.append(f"{hole.strip()}@{domain['name']} discard")

    except KeyError:
        pass

for key in os.environ.keys():
    if key.startswith("RECIPIENT_BCC"):
        recipient_bcc.append(os.environ[key])

for key in os.environ.keys():
    if key.startswith("ALIAS"):
        alias.append(os.environ[key])

if len(alias):
    with open("/etc/aliases", "w") as f:
        for line in alias:
            f.write(line)
            f.write("\n")

    run(["newaliases"])

if len(recipient_bcc):
    with open("/etc/postfix/recipient_bcc", "w") as f:
        for line in recipient_bcc:
            f.write(line)
            f.write("\n")

    run(["postmap", "/etc/postfix/recipient_bcc"])
    run(["postconf", "recipient_bcc_maps=hash:/etc/postfix/recipient_bcc"])

with open("/etc/postfix/transport", "w") as f:
    for line in blackholes:
        f.write(line)
        f.write("\n")

    for line in relay_transport:
        f.write(line)
        f.write("\n")

regex = re.compile('POSTFIX_MAIN_?(.*)')
for key in os.environ.keys():
    match = regex.match(key)

    if match:
        name = match[1]
        value = os.environ[key]
        run(["postconf", f"{name}={value}"])

regex = re.compile('POSTFIX_MASTER_?(.*)')
for key in os.environ.keys():
    match = regex.match(key)

    if match:
        name = match[1].replace("_","/")
        value = os.environ[key]
        run(["postconf", "-eM", f"{name}={value}"])

if "SASLAUTHD_IMAP_SERVER" in os.environ:
    run(["postconf", "-eM", "submission/inet=submission inet n - n - - smtpd -o smtpd_sasl_auth_enable=yes -o smtpd_sasl_path=smtpd"])

run(["postconf", f"relay_domains={', '.join(relay_domains)}"])
run(["postconf", f"relay_recipient_maps={', '.join(relay_recipient_maps)}"])
run(["postconf", f"smtpd_sender_login_maps={', '.join(sender_login_maps)}"])
run(["postconf", "transport_maps=hash:/etc/postfix/transport"])
run(["postmap", "/etc/postfix/transport"])
