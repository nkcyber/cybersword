# modified from https://github.com/a-h/templ/blob/main/examples/counter-basic/Dockerfile

# This Dockerfile builds SQL Injection Lab and hosts
# it on port 8005. It uses the flags from the associated `challenge.yml`s.

# This Dockerfile is meant to be built from the project root,
# as it includes files from both `services` and `challenges`. 

# build lab
FROM golang:alpine3.19 AS build-stage
# RUN apk add --no-cache \
    # # Important: required for go-sqlite3
    # gcc \
    # # Required for Alpine
    # musl-dev
WORKDIR /app
COPY ./services/ai-hacking-lab/ai-hacking-lab .
RUN go mod download
RUN GOOS=linux go build -C /app -o /entrypoint

# build the seed data to include the challenge's flags
FROM python:3.9-slim AS seed-data
WORKDIR /script
# THIS MUST BE UPDATED FOR ALL CHALLENGES USING THE AI LAB
COPY ./services/ai-hacking-lab/create_prompts.py \
    ./services/ai-hacking-lab/requirements.txt \
    .
COPY ./challenges/web/ai-1/challenge.yml ./ai-1.yml
COPY ./challenges/web/ai-2/challenge.yml ./ai-2.yml
RUN pip install -r requirements.txt \
    && python3 create_prompts.py

# deploy as non-root user
FROM golang:alpine3.19 AS release-stage
WORKDIR /app
# TODO SEED DATA
COPY --from=build-stage /app/assets /app/assets
COPY --from=build-stage /app/example-prompts.json .
COPY --from=seed-data /script/prompts.json .
COPY --from=build-stage /entrypoint .
# create and set non-root USER
RUN addgroup -g 1001 appuser && \
    adduser -S -u 1001 -G appuser appuser
RUN chown -R appuser:appuser /app && \
    chmod 755 /app
USER appuser

EXPOSE 8006
ENTRYPOINT ["/app/entrypoint", "-address=0.0.0.0:8006", "-redisAddress=ai-redis:6380", "-ollamaAddress=http://ollama:11434", "-promptPath=./prompts.json"]

