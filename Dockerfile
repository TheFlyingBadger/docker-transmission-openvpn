#
# This Dockerfile generated by createLabelFile.py
# It reads 'DockerfileNoLabels' and then adds
#  some generated label entries
#
# <DockerfileNoLabels>
FROM haugene/transmission-openvpn
ARG container_locale=en_US.UTF-8 
ARG container_language=en_US.en
RUN  apt-get -qqq update  > /dev/null \
    && apt-get -qqq -y install supervisor net-tools lsof inotify-tools python3-pip python3 locales nginx nano > /dev/null \
    && echo .... \
    && echo "Locales ($container_locale - $container_language)" \
    && echo .... \
    && locale-gen $container_locale \
    && update-locale LANG=$container_locale LC_ALL=${container_locale} \
    && cat /etc/default/locale \ 
    && mkdir -p -v /var/log/supervisor \
    && pip3 install  srt humanize transmissionrpc flexget --no-cache-dir  > /dev/null\
    && rm -rf ~/.cache/pip/* \
    && apt-get -q -q clean  > /dev/null \
    && apt-get -q -q autoclean  > /dev/null \
    && ln -s /etc/transmission/environment-variables.sh /etc/profile.d/02-transmission-environment-variables.sh  \
    && chmod +x /etc/transmission/userSetup.sh
ENV LANG $container_locale \
    LANGUAGE $container_language \
    LC_ALL $container_locale \
    TRANSMISSION_HOME=/config/transmission \
    UFW_EXTRA_PORTS=9117,5050,80 \
    XDG_CONFIG_HOME=/config

# Set the locale  
ADD  container/ /

EXPOSE 9117 5050 9091 80
CMD ["/bin/bash","-c","/volansmelesmeles/containerStartup.sh"]
# </DockerfileNoLabels>
#
# LABEL entries added by createLabelFile.py
#
LABEL maintainer="jon@badger.shoes" \
      volansmelesmeles.transmissionopenvpn.base.image.architecture="amd64" \
      volansmelesmeles.transmissionopenvpn.base.image.os="linux" \
      volansmelesmeles.transmissionopenvpn.base.image.repodigests="haugene/transmission-openvpn@sha256:3ada789c4f412ac5bf56bfc0b1c2f4cc1322387c12e01d8821915992f24d8d89" \
      volansmelesmeles.transmissionopenvpn.base.image.repotags="haugene/transmission-openvpn:latest" \
      volansmelesmeles.transmissionopenvpn.base.image="haugene/transmission-openvpn:latest" \
      volansmelesmeles.transmissionopenvpn.jackett.url="https://github.com/Jackett/Jackett/releases/download/v0.14.459/Jackett.Binaries.LinuxAMDx64.tar.gz" \
      volansmelesmeles.transmissionopenvpn.jackett.version="v0.14.459"
