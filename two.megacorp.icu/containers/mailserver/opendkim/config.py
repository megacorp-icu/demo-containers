#!/usr/bin/env python3

import os
import re

domains = {}
keytable = []
signingtable = []
conffile = []

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
    if not "DKIM" in domain:
        continue;

    keytable.append(f"mail._domainkey.{domain['name']} {domain['name']}:mail:/etc/opendkim/keys/{domain['name']}/mail.private")
    signingtable.append(f"*@{domain['name']} mail._domainkey.{domain['name']}")

regex = re.compile('OPENDKIM_?(.*)')
for key in os.environ.keys():
  match = regex.match(key)

  if match:
    name = match[1]
    value = os.environ[key]
    conffile.append(f"{name} {value}")

with open("/etc/opendkim.conf", "w") as f:
    for line in conffile:
        f.write(line)
        f.write("\n")

with open("/etc/opendkim/KeyTable", "w") as f:
    for line in keytable:
        f.write(line)
        f.write("\n")

with open("/etc/opendkim/SigningTable", "w") as f:
    for line in signingtable:
        f.write(line)
        f.write("\n")

with open("/etc/opendkim/TrustedHosts", "w") as f:
    f.write("127.0.0.1\n::1\n10.0.0.0/8\n192.168.0.0/16\n")
