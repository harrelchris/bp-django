# Deploy

Deploy a Python web application to a Debian server with Django and Gunicorn installed in a virtual environment, a Postgres database, NGINX as a reverse proxy and static file server. Secure the server with UFW, and set up TLS with Certbot. Establish continuous delivery using GitHub actions and a webhook.

## Access Token

Create personal access token if the repository is private. 

1. https://github.com/settings/tokens/new
1. Select `repo` scope
1. Generate
1. Copy token
1. Enter the token as your password when prompted by git to authenticate

## Provision Server

Use your preferred cloud provider to create a Debian VM instance. Enable HTTP/HTTPS traffic in the firewall.

1. https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html
1. https://cloud.google.com/compute/docs/instances/create-start-instance

## Configure Server

1. Update packages

    ```shell
    sudo apt update && sudo apt upgrade -y
    ```

1. Install dependencies

    ```shell
    sudo apt install git nginx postgresql python3-venv ufw -y
    ```

1. Set variables

    ```shell
    LOCAL_IP_ADDRESS=111.222.333.444
    POSTGRES_USERNAME=someusername
    POSTGRES_PASSWORD=somepassword
    POSTGRES_DATABASE=somedatabase
    GITHUB_USERNAME=harrelchris
    GITHUB_PASSWORD=abc123abc123abc123
    GITHUB_REPO=bp-django
    SECRET_KEY=$(python3 -c "import secrets;print(secrets.token_urlsafe(64))")
    PUBLIC_IP=$(curl -s -4 ifconfig.me)
    ```

1. Configure UFW

    ```shell
    sudo ufw --force disable
    sudo ufw --force reset
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow https
    sudo sed -i "s/IPV6=no/IPV6=yes/" /etc/default/ufw
    sudo ufw --force disable
    sudo ufw --force enable
    sudo systemctl restart ufw
    ```

1. Create database

    ```shell
    sudo -u postgres psql -c "CREATE USER $POSTGRES_USERNAME WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"
    sudo -u postgres psql -c "CREATE DATABASE $POSTGRES_DATABASE;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DATABASE TO $POSTGRES_USERNAME;"
    ```

1. Install application

    ```shell
    sudo git clone https://$GITHUB_USERNAME:$GITHUB_PASSWORD@github.com/$GITHUB_USERNAME/$GITHUB_REPO.git /srv/web
    sudo python3 -m venv /srv/web/venv
    sudo /srv/web/venv/bin/python3 -m pip install pip setuptools wheel --upgrade --no-cache-dir
    sudo /srv/web/venv/bin/python3 -m pip install gunicorn psycopg2-binary -r /srv/web/requirements.txt --upgrade --no-cache-dir
    sudo cp /srv/web/envs/prod.env /srv/web/.env
    sudo sed -i "s/<SECRET_KEY>/$SECRET_KEY/g" /srv/web/.env
    sudo sed -i "s/<POSTGRES_USERNAME>/$POSTGRES_USERNAME/g" /srv/web/.env
    sudo sed -i "s/<POSTGRES_PASSWORD>/$POSTGRES_PASSWORD/g" /srv/web/.env
    sudo sed -i "s/<POSTGRES_DATABASE>/$POSTGRES_DATABASE/g" /srv/web/.env
    sudo /srv/web/venv/bin/python3 /srv/web/app/manage.py collectstatic
    sudo /srv/web/venv/bin/python3 /srv/web/app/manage.py migrate
    ```

1. Create gunicorn socket and service

    ```shell
    sudo cp /srv/web/deploy/gunicorn.service /etc/systemd/system/gunicorn.service
    sudo cp /srv/web/deploy/gunicorn.socket /etc/systemd/system/gunicorn.socket
    sudo systemctl daemon-reload
    sudo systemctl start gunicorn.socket
    sudo systemctl enable gunicorn.socket
    ```

1. Configure NGINX

    ```shell
    sudo cp /srv/web/deploy/app.conf /etc/nginx/conf.d/app.conf
    sudo sed -i "s/server_name ~^.+$;/server_name $PUBLIC_IP;/" /etc/nginx/conf.d/app.conf
    sudo systemctl restart nginx
    ```

1. Register domain name and configure DNS for your server
    1. https://freenom.com
    1. https://namecheap.com
