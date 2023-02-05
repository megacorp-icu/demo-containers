FROM ubuntu:20:04

WORKDIR /root

COPY kopano.repo z-push.repo /etc/yum.repos.d/

RUN dnf -y install createrepo epel-release 'dnf-command(config-manager)' && \
    mkdir repo && cd repo && \
    curl https://download.kopano.io/community/core%3A/core-11.0.2.51.9684543-RHEL_8-x86_64.tar.gz | tar -xz --strip-components=1 && \
    curl https://download.kopano.io/community/webapp%3A/webapp-6.0.0.57.9dfff09-RHEL_8-noarch.tar.gz | tar -xz --strip-components=1 && \
    createrepo . && \
    dnf config-manager --set-enabled kopano && \
    dnf config-manager --set-enabled z-push && \
    dnf -y install crudini && \
    dnf clean all

COPY configfile.sh wait-for-it.sh /root

CMD /bin/bash
