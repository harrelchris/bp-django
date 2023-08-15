# Update
apt update
apt upgrade -y

# Install dependencies
apt install nginx postgresql python3-venv ufw -y

# Configure UFW
ufw --force disable
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow https
sed -i "s/IPV6=no/IPV6=yes/" /etc/default/ufw
ufw --force disable
ufw --force enable
systemctl restart ufw

# Create database
sudo -u postgres psql -c "CREATE USER $POSTGRES_USERNAME WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $POSTGRES_DATABASE;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DATABASE TO $POSTGRES_USERNAME;"

# Install application
python3 -m venv /srv/web/venv
/srv/web/venv/bin/python3 -m pip install pip setuptools wheel --upgrade --no-cache-dir
/srv/web/venv/bin/python3 -m pip install gunicorn psycopg2-binary -r /srv/web/requirements.txt --upgrade --no-cache-dir
cp /srv/web/envs/prod.env /srv/web/.env
sed -i "s/<SECRET_KEY>/$SECRET_KEY/g" /srv/web/.env
sed -i "s/<POSTGRES_USERNAME>/$POSTGRES_USERNAME/g" /srv/web/.env
sed -i "s/<POSTGRES_PASSWORD>/$POSTGRES_PASSWORD/g" /srv/web/.env
sed -i "s/<POSTGRES_DATABASE>/$POSTGRES_DATABASE/g" /srv/web/.env
/srv/web/venv/bin/python3 /srv/web/app/manage.py collectstatic
/srv/web/venv/bin/python3 /srv/web/app/manage.py migrate

# Create gunicorn socket and service
cp /srv/web/deploy/gunicorn.service /etc/systemd/system/gunicorn.service
cp /srv/web/deploy/gunicorn.socket /etc/systemd/system/gunicorn.socket
systemctl daemon-reload
systemctl start gunicorn.socket
systemctl enable gunicorn.socket

# Configure NGINX
cp /srv/web/deploy/app.conf /etc/nginx/conf.d/app.conf
sed -i "s/server_name ~^.+$;/server_name $PUBLIC_IP;/" /etc/nginx/conf.d/app.conf
systemctl restart nginx
