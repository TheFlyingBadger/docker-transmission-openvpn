#!/bin/bash
. /etc/transmission/userSetup.sh > /dev/null

mkdir -p -v /config/log/supervisor /config/log/nginx/ /config/log/transmission-openvpn /config/log/jackett /config/log/flexget /config/supervisor

export runUser=`id -nu ${PUID}`
export runGroup=`id -ng ${PGID}`


if [ ! -d "/config/nginx" ]; then
    mv /etc/nginx /config/.
    rm /config/nginx/sites-enabled/*
    ln -s /config/nginx/sites-available/* /config/nginx/sites-enabled/.
    ln -s /config/nginx /etc/nginx
    find /config/nginx/. -type f -exec sed -i -e 's=/etc/nginx/=/config/nginx/=g' {} \;
    find /config/nginx/. -type f -exec sed -i -e 's=/var/log/=/config/log/=g' {} \;
    find /config/nginx/. -type f -exec sed -i -e 's=user www-data;=user '${runUser}';=g' {} \;
fi
if [ ! -d "/config/www" ]; then
    mv /var/www /config/.
    ln -s /config/www /var/www
    find /config/nginx/. -type f -exec sed -i -e 's=/var/www/=/config/www/=g' {} \;
fi
if [ ! -f "/config/www/html/index.html" ]; then
    mkdir -p -v /config/www/html/
    mv /var/www/html/index.default.html /config/www/html/index.html
fi
ln -s /config/www/html/index.html /var/www/html/index.html

supervisorConfDefault=/etc/supervisor/supervisord.conf
supervisorConfConfig=/config/supervisor/supervisord.conf
supervisorReadme=/etc/supervisor/readme.txt
if [ -f "${supervisorReadme}" ]; then
    rm ${supervisorReadme}
fi
if [ -f "${supervisorConfConfig}" ]; then
    supervisorConf=$supervisorConfConfig
    echo "${supervisorConfConfig} being used for supervisord" > ${supervisorReadme}
    chown -R $PUID:$PGID ${supervisorReadme}
else
    supervisorConf=$supervisorConfDefault
fi

if [ -f "/config/flexget/.config-lock" ]; then
    rm /config/flexget/.config-lock
fi

chown -R $PUID:$PGID /Jackett /config
su -s /bin/bash -c "python3 /volansmelesmeles/scripts/copyContents.py" ${runUser}
/usr/bin/supervisord -c $supervisorConf