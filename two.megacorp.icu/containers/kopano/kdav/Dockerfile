FROM kopano-base:latest

WORKDIR /root
RUN apt-get update && \
    apt-get -y install php-fpm php-mbstring composer php7-mapi php-xml php-sqlite3 && \
    apt-get clean && \
    mkdir kdav && \
    cd kdav && \
    curl -L https://github.com/Kopano-dev/kdav/tarball/e74884e73b1262c8a69961a9b61fbdf4655fd133 | tar -xz --strip-components=1 && \
    composer install && \
    cd /root && \
    mv kdav /usr/share/ && \
    mkdir -p /var/lib/kopano/kdav && \
    chown -R kopano.kopano /var/lib/kopano/kdav

COPY entrypoint.sh /root
COPY log4php.xml /usr/share/kdav/
COPY fpm-kdav.conf /etc/php/7.4/fpm/pool.d

CMD ["/root/entrypoint.sh"]
