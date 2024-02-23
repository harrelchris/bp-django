#!/usr/bin/env bash

# Update
apt update
apt upgrade -y

# Configure UFW
./srv/web/deploy/ufw.sh

# Create database
./srv/web/deploy/postgres.sh

# Install application
./srv/web/deploy/app.sh

# Create gunicorn socket and service
./srv/web/deploy/gunicorn.sh

# Configure NGINX
./srv/web/deploy/nginx.sh
