FROM kopano-base:latest

WORKDIR /root
RUN dnf -y install kopano-server mariadb && \
    mkdir -p /etc/kopano && \
    dnf clean all

COPY entrypoint.sh /root
CMD /root/entrypoint.sh
