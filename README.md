# docker-transmission-openvpn


This docker container takes the excellent [haugene/transmission-openvpn](https://github.com/haugene/docker-transmission-openvpn) container and extends it to add some of the other tools that would be utilised if you were seeking to download loads of torrents.

As well as the OpenVPN/Tranmission install it also includes.
* [Jackett](https://github.com/Jackett/Jackett) - RSS Proxy Server
* [Flexget](https://flexget.com/) - Automated Torrent processing
* [nginx](https://www.nginx.com/) - Simple lightweight web server

