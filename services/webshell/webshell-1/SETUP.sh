#!/bin/bash

apt-get update && apt-get install python3-pip -y
cat << EOF > /etc/motd
Hi! You're currently running Ubuntu Linux version 22.04.
We recommend using the mouse to select, copy, and paste text.
This terminal will close after 5 minutes to save resources.

You may be used to Graphical User Interfaces, where you point and click to do things.

This is a console. You must type commands to tell the computer what to do.
Your current "prompt" starts with "#". This is where you enter commands.

Try typing two commands:

EOF
# echo green text
echo -e "   \033[38;5;119;48;5;16m # ls \033[0m" >> /etc/motd
cat << EOF >> /etc/motd
    the "ls" command lists the files in the current directory.

EOF
# echo green text
echo -e "   \033[38;5;119;48;5;16m # cat flag.txt \033[0m" >> /etc/motd
cat << EOF >> /etc/motd
    in short, the "cat" command prints the contents of a text file.
    if you just type "cat", it will output whatever you type. type "Ctrl + C" to cancel this command.
    you must tell "cat" what to output. make sure to type the argument "flag.txt".

EOF
printf "\ncat /etc/motd\n# hello!\n" >> /root/.bashrc

cat << "EOF" >> /root/.bashrc
# custom prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

cd "$HOME"
EOF

pip3 install -r /root/SETUP_FILES/requirements.txt
python3 /root/SETUP_FILES/generate_challenge.py

