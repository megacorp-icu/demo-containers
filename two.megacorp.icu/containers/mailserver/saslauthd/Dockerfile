FROM fedora:37

LABEL maintainer="Hein-Pieter van Braam <hp@prehensile-tales.com>"

VOLUME /run/saslauthd

RUN groupadd -r -g 89 postfix && \
    useradd -r -d /var/spool/postfix -g 89 -u 89 -s /sbin/nologin postfix && \
    dnf -y upgrade && \
    dnf -y install aardvark-dns cyrus-sasl cyrus-sasl-plain socat && \
    dnf clean all 

COPY entrypoint.sh /root
RUN chmod +x /root/entrypoint.sh 

CMD ["/root/entrypoint.sh"]

