#!/bin/bash

set -e # exit early on error

apt update && apt install python3-pip vim -y 

cat << EOF > /etc/motd
Hi! You're currently running Ubuntu Linux version 22.04.
Run 'help' for help. 
We recommend using the mouse to select, copy, and paste text.
This terminal will close after 5 minutes to save resources.
EOF
printf "\ncat /etc/motd\n# hello!\n" >> /root/.bashrc

cat << "EOF" >> /root/.bashrc
# custom prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

cd "$HOME"
EOF

pip3 install -r /root/SETUP_FILES/requirements.txt
python3 /root/SETUP_FILES/generate_challenge.py

