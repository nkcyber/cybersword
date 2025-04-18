#!/bin/bash

set -e # stop immediately on errors
set -o pipefail # do not silently ignore errors in pipelines
cd "${0%/*}" # cd into script's current location

## Copy this script onto your machine for easy setup of this repo

if [  -n "$(uname -a | grep Ubuntu)" ]; then
    echo "Ubuntu detected..."
else
    echo "It doesn't look like you're running Ubuntu."
    echo "This script assumes you're on an Ubuntu VM."
    exit 1 # non-zero error code, to indicate error
fi

echo "This script is intended to help set up Cybersword on a new Ubuntu machine."
echo
echo "This script clones the repo recursively."
echo "It should *NOT* be run in the scripts dir."
echo "It should copied to the folder in which you want to install Cybersword."
read -p "Continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
	# handle exits from shell or function but don't exit interactive shell
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi


git config --global credential.helper store # not great for security, great for convinence
echo "If you need to use https authentication with git, create a personal access token:"
printf "\thttps://github.com/settings/tokens\n"
echo ""
git clone --recursive https://github.com/nkcyber/cybersword.git && cd "$(basename "$_" .git)"

# Set up firewall
sudo ufw allow ssh
sudo ufw allow http
sudo ufw enable

echo "Installing CTFd CLI..."
echo "More info: https://github.com/CTFd/ctfcli"

sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install ctfcli

echo "Installing Docker..."
# taken from https://docs.docker.com/engine/install/ubuntu/

# Add Docker's official GPG key:
if ! command -v docker > /dev/null 2>&1; then
  echo "Docker is not installed or not in the PATH."

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
else
  echo "Docker appears to be installed."
fi

echo "Docker has been installed. We recommend rebooting to ensure user permissions are updated."
echo "After rebooting, we recommend running ther other setup scripts in ./cybersword/scripts"
echo "Specifically, consider:"
echo "- set_up_https.sh (optional, for Digital Ocean Droplets)"
echo "- setup_for_ropchain.sh"
echo "- change_flags/interactive_rename.py"
echo "- ctf init"
echo "- add_all_challenges.sh"
echo "- ctf challenge install"

