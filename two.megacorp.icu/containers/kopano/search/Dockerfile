FROM kopano-base:latest

WORKDIR /root
RUN apt-get update && \
    apt-get -y install kopano-search && \
    apt-get clean

COPY entrypoint.sh /root

CMD ["/root/entrypoint.sh"]
