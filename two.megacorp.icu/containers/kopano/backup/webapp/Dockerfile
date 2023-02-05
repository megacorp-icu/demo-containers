FROM kopano-base:latest

WORKDIR /root
RUN dnf -y module enable php:7.4 && \
    dnf -y install kopano-webapp php-fpm && \
    mkdir -p /etc/kopano && \
    mkdir -p /run/php-fpm && \
    mkdir -p /var/lib/kopano-webapp/tmp && \
    dnf clean all

COPY entrypoint.sh /root
COPY configfile.sh /root
COPY fpm-webapp.conf /etc/php-fpm.d/

CMD /root/entrypoint.sh
