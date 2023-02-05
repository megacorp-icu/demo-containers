FROM fedora:37

LABEL maintainer="Hein-Pieter van Braam <hp@prehensile-tales.com>"

VOLUME /var/spool/postfix
VOLUME /var/spool/postfix/sockets

EXPOSE 25/tcp
EXPOSE 465/tcp

RUN groupadd -r -g 89 postfix && \
    useradd -r -d /var/spool/postfix -g 89 -u 89 -s /sbin/nologin postfix && \
    dnf -y upgrade && \
    dnf -y install aardvark-dns postfix postfix-ldap cyrus-sasl cyrus-sasl-plain nagios-plugins-smtp && \
    dnf clean all

COPY entrypoint.sh /root
COPY config.py /root
RUN chmod +x /root/entrypoint.sh /root/config.py

CMD ["/root/entrypoint.sh"]

