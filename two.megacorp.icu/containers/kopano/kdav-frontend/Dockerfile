FROM kopano-kdav:latest

WORKDIR /root
RUN apt-get update && \
    apt-get -y install nginx && \
    apt-get clean

COPY nginx.conf /etc/nginx
COPY default /etc/nginx/sites-available/default
COPY entrypoint.sh /root

CMD ["/root/entrypoint.sh"]
