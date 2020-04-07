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
ENV LANG $container_locale
ENV LANGUAGE $container_language
ENV LC_ALL $container_locale
# Set the locale  
ADD  root/ /

EXPOSE 9117 5050 9091
CMD ["/bin/bash","-c","/volansmelesmeles/containerStartup.sh"]
