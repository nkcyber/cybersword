# This Dockerfile downloads "gotty" and sets up the 
# Dockerfile and start-shell script, so that users can
# interact with a console in their browsers.

# all paths are relative to the git root directory

FROM golang:1.22 AS download-gotty

RUN go install github.com/sorenisanerd/gotty@v1.5.0

FROM docker:26-dind AS webshell-host

WORKDIR /app

COPY --from=download-gotty /go/bin/gotty /app/gotty

# https://stackoverflow.com/a/35613430
RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2

# copy into image for setup (it will be deleted before the final image)
COPY ./services/webshell/webshell-4/SETUP.sh SETUP.sh
COPY ./services/webshell/webshell-4/start-shell.sh start-shell.sh

# create the dockerfile for this challenge
RUN <<EOF
cat <<HEREDOC > Dockerfile
# The basic dockerfile that is loaded for each console.
# should take ~1MB per open console.
FROM ubuntu:22.04 

# the normal $HOME equals "/root"
WORKDIR /root

# set up files and scripts
COPY SETUP.sh SETUP.sh
COPY SETUP_FILES SETUP_FILES/
RUN bash SETUP.sh
RUN rm SETUP.sh
RUN rm -rf SETUP_FILES/

# Start the new bash shell 
CMD ["/bin/bash", "--rcfile", "/tmp/config.sh"]
HEREDOC
EOF

# run docker containers inside this docker container.
# therefore, each client is isolated from each other
CMD ["/app/gotty", "--port", "9040", "--path", "/webshell-4", "-w", "/bin/sh", "start-shell.sh"]

EXPOSE 9040

