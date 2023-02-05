FROM ubuntu:20.04

WORKDIR /root

COPY sources.list /etc/apt/sources.list

RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo UTC > /etc/timezone && \
    apt-get -y update && \
    apt-get -y install curl dpkg-dev tzdata crudini monitoring-plugins-basic && \
    mkdir /repo && cd /repo && \
    curl https://download.kopano.io/community/core%3A/core-11.0.2.51.c08b7f4-Ubuntu_20.04-amd64.tar.gz | tar -xz --strip-components=1 && \
    curl https://download.kopano.io/community/webapp%3A/webapp-6.0.0.66.43d5c5d-Ubuntu_20.04-all.tar.gz | tar -xz --strip-components=1 && \
    curl https://download.kopano.io/community/archiver%3A/archiver-11.0.2.51.f9ea400-Ubuntu_20.04-amd64.tar.gz | tar -xz --strip-components=1 && \
    dpkg-scanpackages . /dev/null > Packages && \
    chown -R _apt /repo && \
    echo 'deb [trusted=yes] file:///repo ./' >> /etc/apt/sources.list && \
    echo 'kopano:x:999:999:Kopano Groupware Suite:/dev/null:/sbin/nologin' >> /etc/passwd && \
    echo 'kopano:!:19142::::::' >> /etc/shadow && \
    echo 'kopano:x:999:' >> /etc/group && \
    apt-get -y update && \
    apt-get -y install kopano-client kopano-common && \
    apt-get -y remove dpkg-dev && \
    apt-get -y autoremove && \
    apt-get clean 
    
COPY configfile.sh wait-for-it.sh php_configfile.sh /root

CMD /bin/bash
