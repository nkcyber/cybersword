#!/bin/bash

set -e # stop immediately on errors
set -o pipefail # do not silently ignore errors in pipelines
cd "${0%/*}" # cd into script's current location
cd .. # cd into the root directory of the project

## Copy this script onto your machine for easy setup of this repo

if [  -n "$(uname -a | grep Ubuntu)" ]; then
    echo "Ubuntu detected..."
else
    echo "It doesn't look like you're running Ubuntu."
    echo "This script assumes you're on an Ubuntu VM."
    exit 1 # non-zero error code, to indicate error
fi  

git config --global credential.helper store # not great for security, great for convinence
echo "If you need to use https authentication with git, create a personal access token:"
printf "\thttps://github.com/settings/tokens\n"
git clone https://github.com/nkcyber/advent-of-everything.git --recursive

cd advent-of-everything

echo "Installing Docker"
# taken from https://docs.docker.com/engine/install/ubuntu/

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo systemctl enable docker.service
sudo systemctl enable containerd.service

sudo usermod -aG docker $USER

echo "Docker has been installed. We recommend rebooting to ensure user permissions are updated."