#!/usr/bin/env python3

import os
import re

lines = []

regex = re.compile('SPAMASSASSIN_?(.*)')
for key in os.environ.keys():
  match = regex.match(key)

  if match:
    name = match[1].lower()
    value = os.environ[key]
    lines.append(f"{name} {value}")

regex = re.compile('SPAM_SCORE_?(.*)')
for key in os.environ.keys():
  match = regex.match(key)

  if match:
    name = match[1]
    value = os.environ[key]
    lines.append(f"score {name} {value}")

with open("/etc/mail/spamassassin/local.cf", "w") as f:
  for line in lines:
    f.write(line)
    f.write("\n")
