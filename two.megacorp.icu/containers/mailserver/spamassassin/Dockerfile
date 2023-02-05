FROM fedora:37

LABEL maintainer="Hein-Pieter van Braam <hp@prehensile-tales.com>"

VOLUME /var/spool/postfix/sockets
VOLUME /var/lib/mail/spamassassin

WORKDIR /root

RUN groupadd -r -g 89 postfix && \
    useradd -r -d /var/spool/postfix -g 89 -u 89 -s /sbin/nologin postfix && \
    dnf -y upgrade && \
    dnf -y install aardvark-dns spamassassin spamass-milter rsyslog python3-pip git crudini pyzor socat && \
    dnf clean all && \
    pip3 install inotify && \
    git clone https://github.com/PrehensileTales/inotify-spamlearn.git && \
    mv inotify-spamlearn/inotify-spamlearn.cfg /etc/inotify-spamlearn.cfg && \
    mv inotify-spamlearn/inotify-spamlearn.py /usr/local/bin/inotify-spamlearn.py && \
    rm -rf inotify-spamlearn 

COPY entrypoint.sh /root
COPY spamassassin-config.py /root
COPY rsyslog.conf /etc

RUN chmod +x /root/entrypoint.sh /root/spamassassin-config.py

ENTRYPOINT ["/root/entrypoint.sh"]

