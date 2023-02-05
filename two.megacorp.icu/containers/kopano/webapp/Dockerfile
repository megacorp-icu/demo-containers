FROM kopano-base:latest

WORKDIR /root
RUN apt-get update && \
    apt-get -y install kopano-webapp php-fpm git && \
    git clone https://github.com/PrehensileTales/kopano-web-client-night-theme.git && \
    mv kopano-web-client-night-theme/iconsets/* /usr/share/kopano-webapp/client/resources/iconsets && \
    mv kopano-web-client-night-theme/plugins/* /usr/share/kopano-webapp/plugins && \
    rm -rf kopano-web-client-night-theme && \
    apt-get -y remove git && \
    apt-get -y autoremove && \
    mkdir -p /etc/kopano && \
    mkdir -p /run/php-fpm && \
    mkdir -p /var/lib/kopano-webapp/tmp && \
    apt-get clean && \
    crudini --set /etc/php/7.4/fpm/php.ini PHP post_max_size 128M && \
    crudini --set /etc/php/7.4/fpm/php.ini PHP upload_max_filesize 120M 

COPY entrypoint.sh /root
COPY fpm-webapp.conf /etc/php/7.4/fpm/pool.d

CMD ["/root/entrypoint.sh"]
