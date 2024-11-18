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
COPY ./services/webshell/ropchain-1/SETUP.sh SETUP.sh
COPY ./services/webshell/ropchain-1/start-shell.sh start-shell.sh

# Copy Dockerfile that will be used to create interactive clients
# This is responsible for running SETUP.sh and using generate_challenge.py
COPY ./services/webshell/ropchain-1/ropchain-lab/ .

# run docker containers inside this docker container.
# therefore, each client is isolated from each other
CMD ["/app/gotty", "--port", "9050", "--path", "/ropchain-1", "-w", "/bin/sh", "start-shell.sh"]

EXPOSE 9050

