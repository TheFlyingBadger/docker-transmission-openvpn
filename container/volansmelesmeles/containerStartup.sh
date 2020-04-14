#!/bin/bash
. /etc/transmission/userSetup.sh > /dev/null

mkdir -p -v /config/log/supervisor /config/log/nginx/ /config/log/transmission-openvpn /config/log/jackett /config/log/flexget /config/supervisor /config/log/addTrackers/

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

if [ ! -d "/data/transmission-home" ]; then
    ln -s /config/transmission /data/transmission-home
fi

mkdir -p -v /config/tinyproxy
tinyproxyConf=/config/tinyproxy/tinyproxy.conf
if [ ! -f "${tinyproxyConf}" ]; then
    mv /etc/tinyproxy/tinyproxy.conf /config/tinyproxy/.
    ln -s $tinyproxyConf /etc/tinyproxy/tinyproxy.conf 
fi

if [ ! -d /config/tinyproxy/tinyproxy ]; then
    mv /usr/share/tinyproxy /config/tinyproxy/.
    ln -s /config/tinyproxy/tinyproxy /usr/share/tinyproxy
fi
sed -i -e 's=/var/log/tinyproxy=/config/log/transmission-openvpn=g' $tinyproxyConf
ln -s /config/log/transmission-openvpn/tinyproxy.log /var/log/tinyproxy.log

# stop the "sed" calls in tinyproxy start.sh from breaking our symlink
sed -i -e 's,sed -i -e,sed -i --follow-symlinks -e,g' /opt/tinyproxy/start.sh 

chown -R $PUID:$PGID /Jackett /config
su -s /bin/bash -c "python3 /volansmelesmeles/scripts/copyContents.py" ${runUser}
/usr/bin/supervisord -c $supervisorConf