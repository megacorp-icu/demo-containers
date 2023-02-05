FROM kopano-base:latest

WORKDIR /root
RUN apt-get update && \
    apt-get -y install gnupg && \
    echo "deb https://download.kopano.io/zhub/z-push%3A/final/Ubuntu_20.04/ /" >> /etc/apt/sources.list && \
    curl https://download.kopano.io/zhub/z-push%3A/final/Ubuntu_20.04/Release.key | apt-key add - && \
    apt-get update && \
    apt-get -y install z-push-common z-push-backend-kopano z-push-ipc-sharedmemory z-push-autodiscover php-fpm php-mbstring && \
    apt-get clean 

COPY entrypoint.sh /root
COPY fpm-z-push.conf /etc/php/7.4/fpm/pool.d

CMD ["/root/entrypoint.sh"]
