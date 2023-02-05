#!/usr/bin/python3

import os
import re
import shutil
from subprocess import run, PIPE

suffixes = {}
replicas = {}
use_memberof = False

re_key = re.compile('INITIAL_SUFFIX_([0-9]+)_?(.*)')
re_rep = re.compile('REPLICA_([0-9]+)_HOST_?(.*)')

for key in os.environ.keys():
  match = re_key.match(key)

  if match:
    i = match[1]
    if not i in suffixes: suffixes[i] = {}

    if not match[2]:
      suffixes[i]['dn'] = os.environ[key]
    else:
      suffixes[i][match[2]] = os.environ[key]

  match = re_rep.match(key)
  if match:
    replicas[match[1]] = os.environ[key]

for idx, suffix in suffixes.items():
  if not 'ORGANIZATION' in suffix:
    print(f"Error: Suffix {suffix['dn']} does not have an organization")
    exit(1)

  if 'USE_MEMBEROF' in suffix:
    if suffix['USE_MEMBEROF'] == "1": use_memberof = True

rootpw = ""
if 'INITIAL_ROOTPW' in os.environ:
  if len(os.environ['INITIAL_ROOTPW']) > 0:
    rootpw = os.environ['INITIAL_ROOTPW']
    del os.environ['INITIAL_ROOTPW']

if not rootpw:
  rootpw = run(['pwgen', '10'], stdout=PIPE).stdout.decode().strip()

rootpw_encoded = run(['slappasswd', '-s', rootpw], stdout=PIPE).stdout.decode().strip()

readpw = run(['pwgen', '10'], stdout=PIPE).stdout.decode().strip()
readpw_encoded = run(['slappasswd', '-s', readpw], stdout=PIPE).stdout.decode().strip()

config_ldif="""
dn: cn=config
objectClass: olcGlobal
cn: config
olcDisallows: bind_anon
olcLogLevel: 11
olcSaslSecProps: none
olcTLSCACertificatePath: /etc/pki/ca-trust/extracted/pem/directory-hash
olcTLSCertificateFile: /data/ssl/fullchain.pem
olcTLSCertificateKeyFile: /data/ssl/privkey.pem
olcTLSCipherSuite: ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305
 :ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES2
 56-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA
 -AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-
 ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-A
 ES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA
 256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA
 -DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256
 :AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CB
 C3-SHA:!DSS
olcTLSDHParamFile: /data/ssl/slapd.dh.params
olcTLSProtocolMin: 3.3

dn: cn=module,cn=config
objectClass: olcModuleList
cn: module
olcModulepath: /usr/lib64/openldap
olcModuleLoad: syncprov
"""
if use_memberof:
  config_ldif += "olcModuleLoad: memberof\n"

config_ldif += """

dn: cn=schema,cn=config
objectClass: olcSchemaConfig
cn: schema

"""

schemas = []
if 'INITIAL_SCHEMAS' in os.environ:
  schemas = os.environ['INITIAL_SCHEMAS'].split(" ")

if not 'core' in schemas:
  schemas.append('core')

for schema in schemas:
  config_ldif += f"include: file:///etc/openldap/schema/{schema}.ldif\n"

config_ldif += f"""
dn: olcDatabase=config,cn=config
objectClass: olcDatabaseConfig
olcDatabase: config
olcAccess: to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" manage by * none
olcRootDN: cn=manager,cn=config
olcRootPW: {rootpw_encoded}
"""

if replicas:
  config_ldif += f"olcMultiProvider: TRUE\n"
  replica_num = 0
  for id, host in replicas.items():
    config_ldif += f'olcSyncrepl: { {replica_num} }rid={id} provider=ldaps://{host} binddn="cn=manager,cn=config" bindmethod=simple credentials={rootpw} searchbase="cn=config" type=refreshAndPersist retry="10 +" timeout=1\n'
    replica_num += 1

config_ldif += f"""
dn: olcOverlay={{0}}syncprov,olcDatabase={{0}}config,cn=config
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: {{0}}syncprov

dn: olcDatabase=monitor,cn=config
objectClass: olcDatabaseConfig
olcDatabase: monitor
olcAccess: to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" read by * none
"""

db_num = 2
for idx, suffix in suffixes.items():
  os.mkdir(f"/data/databases/{suffix['dn']}")
  if 'ROOTPW' in suffix:
    suffix_rootpw_encoded = run(['slappasswd', '-s', suffix['ROOTPW']], stdout=PIPE).stdout.decode().strip()

  overlay_num = 1
  config_ldif += f"""
dn: olcDatabase=mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: mdb
olcSuffix: {suffix['dn']}
olcRootDN: cn=Manager,{suffix['dn']}
"""

  if 'ROOTPW' in suffix:
    config_ldif += f"olcRootPW: {suffix_rootpw_encoded}"

  config_ldif += f"""
olcDbDirectory: /data/databases/{suffix['dn']}
olcDbIndex: objectClass eq,pres
olcDbIndex: ou,cn,mail,surname,givenname eq,pres,sub
olcAccess: {{0}}to attrs=userPassword by group.exact="cn=LDAP Server Administrators,ou=groups,{suffix['dn']}" write by self =wx by anonymous auth by dn.base=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth write by * none
olcAccess: {{1}}to * by dn.base=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth write by group.exact="cn=LDAP Server Administrators,ou=groups,{suffix['dn']}" write by dn.exact=uid=read,ou=systemusers,{suffix['dn']} read by * read
"""

  if replicas:
    config_ldif += f"olcMultiProvider: TRUE\n"
    replica_num = 0
    for id, host in replicas.items():
      config_ldif += f'olcSyncrepl: { {replica_num} }rid={id} provider=ldaps://{host} binddn="cn=manager,{suffix["dn"]}" bindmethod=simple credentials={suffix["ROOTPW"]} searchbase="{suffix["dn"]}" type=refreshAndPersist retry="10 +" timeout=1\n'
      replica_num += 1

  config_ldif += f"""
dn: olcOverlay={{0}}syncprov,olcDatabase={ {db_num} }mdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: {{0}}syncprov
"""

  if 'USE_MEMBEROF' in suffix and suffix['USE_MEMBEROF'] == '1':
    config_ldif += f"""
dn: olcOverlay={ {overlay_num} }memberof,olcDatabase={ {db_num} }mdb,cn=config
objectClass: olcConfig
objectClass: olcMemberOf
objectClass: olcOverlayConfig
objectClass: top
olcOverlay: { {overlay_num} }memberof
olcMemberOfDangling: drop
olcMemberOfGroupOC: groupOfNames
olcMemberOfMemberAD: member
olcMemberOfMemberOfAD: memberOf
olcMemberOfRefInt: TRUE
"""
    overlay_num += 1

  db_num += 1

print("Loading cn=config ldif")
print(config_ldif)
out = run(['/usr/sbin/slapadd', '-F', '/data/conf.d', '-n0'], stdout=PIPE, input=config_ldif, encoding='ascii')
print(out.stdout)
if out.returncode:
  print("Error:") 
  print(out.stderr)
  exit(1)
else:
  print("Success!")

for idx, suffix in suffixes.items():
  suffix_ldif=f"""
dn: {suffix['dn']}
objectClass: dcObject
objectClass: organization
dc: {suffix['dn'].split("=")[1].split(",")[0]}
o: {suffix['ORGANIZATION']}

dn: ou=systemusers,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: systemusers

dn: uid=nobody,ou=systemusers,{suffix['dn']}
objectClass: account
objectClass: top
uid: nobody

dn: uid=read,ou=systemusers,{suffix['dn']}
objectClass: account
objectClass: simpleSecurityObject
objectClass: top
uid: read
userPassword: {readpw_encoded}

dn: ou=users,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: users

dn: ou=groups,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: groups

dn: ou=LDAP Server Administrators,ou=groups,{suffix['dn']}
objectClass: groupOfNames
objectClass: top
cn: LDAP Server Administrators
member: uid=nobody,ou=systemusers,{suffix['dn']}

dn: ou=mailboxes,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: mailboxes

dn: ou=external,ou=users,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: external

dn: ou=internal,ou=users,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: internal

dn: ou=applications,ou=groups,{suffix['dn']}
objectClass: organizationalUnit
objectClass: top
ou: applications

"""

  print(f"Loading {suffix['dn']} ldif")
  print(suffix_ldif)
  out = run(['/usr/sbin/slapadd', '-F', '/data/conf.d', '-b', suffix['dn']], stdout=PIPE, input=suffix_ldif, encoding='ascii')
  print(out.stdout)
  if out.returncode:
    print("Error:") 
    print(out.stderr)
    exit(1)

print(f"Note: cn=manager,cn=config password is {rootpw}")
print(f"Note: uid=read,ou=systemusers password is {readpw}")
print("Note: this note will not be repeated!")
