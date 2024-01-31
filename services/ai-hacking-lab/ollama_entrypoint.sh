#!/bin/sh

./bin/ollama serve &

sleep 5

# depends on `ollama` service in docker-compose.yml
curl -X POST http://ollama:11434/api/pull -d '{"name": "tinyllama"}'

sleep 10

tail -f /dev/null
