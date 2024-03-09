#!/bin/bash

set -e # stop immediately on errors
set -o pipefail # do not silently ignore errors in pipelines
cd "${0%/*}" # cd into script's current location
cd .. # cd into the root directory of the project

if [  -n "$(uname -a | grep Ubuntu)" ]; then
    echo "Ubuntu detected..."
else
    echo "It doesn't look like you're running Ubuntu."
    echo "This script uses snap and ufw, which may not exist on other Linux distros."
    exit 1 # non-zero error code, to indicate error
fi  

echo "Ensuring server is down..."
docker compose down

echo "enter the domain name you want to set up https certs for:"
read DOMAIN_NAME

read -p "set up https for '$DOMAIN_NAME'? (y/n) " -n 1 -r
echo "" # add newline after user input
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo snap install core; sudo snap refresh core
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    sudo ufw allow http
    sudo ufw allow https
    sudo certbot certonly --standalone -d "$DOMAIN_NAME" --agree-tos  --no-eff-email
    # create symlink for docker to read from regardless of domain name
    sudo ln -s "/etc/letsencrypt/live/$DOMAIN_NAME" /etc/letsencrypt/cybersword
fi

