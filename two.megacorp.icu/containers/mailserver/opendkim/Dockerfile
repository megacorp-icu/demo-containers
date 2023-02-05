FROM fedora:37

LABEL maintainer="Hein-Pieter van Braam <hp@prehensile-tales.com>"

VOLUME /etc/opendkim

RUN groupadd -r -g 89 postfix && \
    useradd -r -d /var/spool/postfix -g 89 -u 89 -s /sbin/nologin postfix && \
    dnf -y upgrade && \
    dnf -y install aardvark-dns opendkim opendkim-tools rsyslog socat && \
    dnf clean all

COPY entrypoint.sh /root
COPY config.py /root
COPY rsyslog.conf /etc
RUN chmod +x /root/entrypoint.sh /root/config.py

CMD ["/root/entrypoint.sh"]

