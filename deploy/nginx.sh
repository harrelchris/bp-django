#!/usr/bin/env bash

apt install nginx -y

cp /srv/web/deploy/app.conf /etc/nginx/conf.d/app.conf

# Set the server name to the public IP address
# PUBLIC_IP=$(curl -s -4 ifconfig.me)
# sed -i "s/server_name ~^.+$;/server_name $PUBLIC_IP;/" /etc/nginx/conf.d/app.conf

systemctl restart nginx
systemctl enable nginx
systemctl daemon-reload
