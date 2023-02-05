## Simple OpenLDAP container.
[![Docker Repository on Quay.io](https://quay.io/repository/tmm/openldap/status "Docker Repository on Quay.io")](https://quay.io/repository/tmm/openldap)

This container installs a simple non-replicated OpenLDAP server. All data is stored on the `/data/` volume. By default ACLs are created that allow modification of entries through LDAPI, with userPassword field being protected.

## Running
The container is build by Quay.io at `quay.io/tmm/openldap`.

The following environment variables affect the runtime behavior of the container:

* `SLAPD_LISTEN_LDAPS` Listen to LDAPS (port 636) defaults to `1`
* `SLAPD_LISTEN_LDAP` Listen to LDAP (port 389) defaults to `1`
* `SLAPD_LISTEN_LDAPI` Listen to LDAPI (/data/ldapi) defaults to `1`
* `SLAPD_LOGLEVEL` Set the SLAPD loglevel. Defaults to `2`

## Configuration
The following environment variables affect the initial configuration:

### Password
Environment variable: `INITIAL_ROOTPW`
The initial root password for cn=config. The name for the root account is cn=manager,cn=config. If this is not set a random password will be generated and will be printed the first time the container starts up. This will not be repeated on subsequent starts.

### Initial schemas
Environment variable: `INITIAL_SCHEMAS`
Set the initial schemas to be loaded into the directory. These are the schemas shipped by OpenLDAP. The following schemas are shipped with this container:
* collective
* corba
* core
* cosine
* duaconf
* dyngroup
* inetorgperson
* java
* misc
* nis
* openldap
* pmi
* ppolicy

By default the container loads `core cosine inetorgperson`. The `core` schema is always loaded regardless of user settings. When the `ppolicy` overlay is requested this schema will also be loaded automatically.

### Default databases
The container can make one or more databases based on environment variables:
* `INITIAL_SUFFIX_X` BaseDN for the suffix (Mandatory)
* `INITIAL_SUFFIX_X_ORGANIZATION` Organization name for the suffix base object. (dcobject, organization) (Mandatory)
* `INITIAL_SUFFIX_X_USE_PPOLICY` Enable the ppolicy overlay for this suffix. (loads overlay automatically, creates a `cn=default,ou=policies,dc=base,dc=dn` object)
* `INITIAL_SUFFIX_X_USE_PPOLICY_HASH_CLEARTEXT` The directory will hash non EXOP password changes and check their password strength. This will make it impossible to directly set hashed `userPassword` fields.
* `INITIAL_SUFFIX_X_USE_PPOLICY_USE_PWCHECK` Enable the `check_password.so` password checker for additional password checks.
* `INITIAL_SUFFIX_X_USE_MEMBEROF` Enable the 'memberof' reverse mapping between users and groups. Configured for GroupOfNames.

Where the 'X' can be replaced by a number. Multiple databases can be created this way.

Note that root passwords can not be set in this manner, use the `ldapi:///` interface or the `cn=manager,cn=config` user.

Allows the creation of initial suffixes when the container is first started. By default:
```
INITIAL_SUFFIX_1 dc=example,dc=com
INITIAL_SUFFIX_1_ORGANIZATION Example organization
INITIAL_SUFFIX_1_USE_PPOLICY 1
INITIAL_SUFFIX_1_USE_PPOLICY_HASH_CLEARTEXT 1
INITIAL_SUFFIX_1_USE_PPOLICY_USE_PWCHECK 1
INITIAL_SUFFIX_1_USE_MEMBEROF 1
```

### Pwcheck
The container can configure the pwcheck module. If the pwcheck module isn't in use these settings have no effect:
* `PWCHECK_MINPOINTS` Minimum number of quality points a new password must have to be accepted. One quality point is awarded for each character class used in the password.
* `PWCHECK_MINUPPER` Minimum upper characters expected.
* `PWCHECK_MINLOWER` Minimum lower characters expected.
* `PWCHECK_MINDIGIT` Minimum digit characters expected.
* `PWCHECK_MINPUNCT` Minimum punctuation characters expected.

By default:
```
PWCHECK_MINPOINTS 3
PWCHECK_MINUPPER 0
PWCHECK_MINLOWER 0
PWCHECK_MINDIGIT 0
PWCHECK_MINPUNCT 0
```

