#!/bin/bash

set -e # exit early on error

apt-get update && apt-get install python3-pip tmux vim nano -y

cat << EOF > /etc/motd
Hi! You're currently running Ubuntu Linux version 22.04.
We recommend using the mouse to select, copy, and paste text.
This terminal will close after 30 minutes to save resources.

When you are done, please type "exit".

Tools on this machine:
	- python3
	- ipython
	- vim
	- nano
	- tmux

Good luck!
EOF

cat << EOF >> /root/.bashrc
# custom prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

cd "$HOME"
EOF

pip3 install -r /root/SETUP_FILES/requirements.txt
python3 /root/SETUP_FILES/generate_challenge.py

