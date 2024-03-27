#!/bin/bash

set -e # exit early on error

apt-get update && apt-get install python3-pip -y

cat << EOF > /etc/motd
Hi! You're currently running Ubuntu Linux version 22.04.
We recommend using the mouse to select, copy, and paste text.
This terminal will close after 5 minutes to save resources.

You learned that the command "ls" lists the files in the current directory.

You can use the flag "-a" to list all of the files, including hidden files.
EOF

echo -e "   \033[38;5;119;48;5;16m # ls -a \033[0m" >> /etc/motd

cat << EOF >> /etc/motd
This should list several directories, including ".hidden_directory"

Then, use "cd" to change directory into ".hidden_directory".
Then, use "ls -a" again to see the hidden file containing the flag.
EOF

printf "\ncat /etc/motd\n# hello!\n" >> /root/.bashrc

cat << "EOF" >> /root/.bashrc
# custom prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

cd "$HOME"
EOF

pip3 install -r /root/SETUP_FILES/requirements.txt
python3 /root/SETUP_FILES/generate_challenge.py

