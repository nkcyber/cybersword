#!/bin/sh

set -e

# This script is loaded by gotty, and is in charge of starting a jailed and virtualized console.
# This script is loaded by "Dockerfile"

CONTAINER_NAME="challenge-shell-$(uuidgen)"
CONTAINER_TAG="webshell"
TIMEOUT="300" # 300 seconds = 5 minutes

# Build image from the challenge's Dockerfile and SETUP.sh
# This takes a moment, but I don't think there's a way to build
# a docker image during the build step of another image.
docker build --tag "$CONTAINER_TAG" .

clear # clear output

(sleep "$TIMEOUT" ; echo "Out of time after $TIMEOUT seconds! Refresh to try again." ; docker stop $CONTAINER_NAME)&

docker run -m 15M --cpu-quota 3000 --name "$CONTAINER_NAME" -it --rm "$CONTAINER_TAG"


