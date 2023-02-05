FROM kopano-base:latest

WORKDIR /root
RUN dnf -y config-manager --set-enabled powertools && \
    dnf -y install kopano-search && \
    dnf clean all

COPY entrypoint.sh /root
COPY configfile.sh /root
COPY fpm-webapp.conf /etc/php-fpm.d/

CMD /root/entrypoint.sh
