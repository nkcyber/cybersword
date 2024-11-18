#!/bin/bash

set -e # exit early on error


RED="\e[31m"
GREEN="\e[32m"
LIGHTGREEN="\e[92m"
BOLDGREEN="\e[1;32m"
BOLDITALICRED="\e[1;3;31m"
FILECOLOR="\e[1;92m"
EXECCOLOR="\e[41;37m"
ENDCOLOR="\e[0m"

cat << EOF > /etc/motd
Hi! You're currently running Debian GNU/Linux 12 (bookworm).
We recommend using the mouse to select, copy, and paste text.
This terminal will close after ${BOLDITALICRED}30 minutes${ENDCOLOR} to save resources.

Here's an overview of the files you're working with:
   - ${FILECOLOR}example.c${ENDCOLOR} was compiled to produce:
     - ${EXECCOLOR}./example${ENDCOLOR}, a root-owned Set-UID binary
     - ${LIGHTGREEN}./example-crash${ENDCOLOR}, a normal binary (for analysis)
   - ${FILECOLOR}attack.py${ENDCOLOR}
     - You can edit it with ${GREEN}nano attack.py${ENDCOLOR} or ${GREEN}vim attack.py${ENDCOLOR}.
     - You can run it with ${GREEN}./attack.py${ENDCOLOR} or ${GREEN}python3 attack.py${ENDCOLOR}
   - ${FILECOLOR}create_table.py${ENDCOLOR} (you can run this with ${LIGHTGREEN}./create_table.py${ENDCOLOR})
   - ${FILECOLOR}flag.txt${ENDCOLOR} (only readable as root)

Good luck!

EOF

cat << 'EOF' >> /home/user/.bashrc
if [ -f /etc/motd ]; then
    printf "$(cat /etc/motd)"
    echo ""
fi
EOF

unset RED
unset GREEN
unset LIGHTGREEN
unset BOLDGREEN
unset BOLDITALICRED
unset FILECOLOR
unset EXECCOLOR
unset ENDCOLOR

python3 /app/SETUP_FILES/generate_challenge.py

