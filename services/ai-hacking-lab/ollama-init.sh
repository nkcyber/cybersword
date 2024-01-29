#!/bin/bash sh

set -e # stop immediately on errors
set -o pipefail # do not silently ignore errors in pipelines

# TO BE INCLUDED BY docker-compose.yml

echo "initalizing ollama"

systemctl enable ollama
ollama pull tinygo # must match model in Dockerfile

