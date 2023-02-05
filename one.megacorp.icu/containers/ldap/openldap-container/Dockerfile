FROM fedora:36

LABEL maintainer="Hein-Pieter van Braam <hp@prehensile-tales.com>"

VOLUME /data
EXPOSE 389/tcp
EXPOSE 636/tcp

RUN dnf -y install openldap-servers openldap-clients pwgen openssl && \
    dnf -y upgrade ca-certificates && \
    dnf clean all && \
    mkdir -p /data && \
    chown ldap.ldap /data && \
    trust extract-compat

COPY startslapd.sh /usr/local/sbin
COPY createconfig.py /usr/local/sbin

RUN chmod +x /usr/local/sbin/startslapd.sh 

ENV INITIAL_SCHEMAS="core cosine inetorgperson" \
    INITIAL_SUFFIX_1=dc=example,dc=com \
    INITIAL_SUFFIX_1_ORGANIZATION="Example organization" \
    INITIAL_SUFFIX_1_USE_MEMBEROF=1 \
    INITIAL_ROOTPW="" \
    SLAPD_LISTEN_LDAPS=1 \
    SLAPD_LISTEN_LDAP=1 \
    SLAPD_LISTEN_LDAPI=1 \
    SLAPD_LOGLEVEL=2

CMD /usr/local/sbin/startslapd.sh
