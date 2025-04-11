# modified from https://github.com/a-h/templ/blob/main/examples/counter-basic/Dockerfile

# This Dockerfile builds SQL Injection Lab and hosts
# it on port 8005. It uses the flags from the associated `challenge.yml`s.

# This Dockerfile is meant to be built from the project root,
# as it includes files from both `services` and `challenges`. 

# build lab
FROM golang:alpine3.19 AS build-stage
RUN apk add --no-cache \
    # Important: required for go-sqlite3
    gcc \
    # Required for Alpine
    musl-dev
WORKDIR /app
COPY ./services/sql-injection-lab/sql-injection-lab .
RUN go mod download
RUN CGO_ENABLED=1 GOOS=linux go build -C /app -o /entrypoint

# build the seed data to include the challenge's flags
FROM python:3.9-slim AS seed-data
WORKDIR /script
COPY ./services/sql-injection-lab/create_seed_data.py \
    ./services/sql-injection-lab/requirements.txt \
    .
COPY ./challenges/sql/basic_injection/challenge.yml ./basic_injection.yml
COPY ./challenges/sql/union_injection/challenge.yml ./union_injection.yml
COPY ./challenges/sql/schema_injection/challenge.yml ./schema_injection.yml
RUN pip install -r requirements.txt \
    && python3 create_seed_data.py

# deploy as non-root user
FROM golang:alpine3.19 AS release-stage
WORKDIR /app
COPY --from=seed-data /script/seed_data.sql .
COPY --from=build-stage /entrypoint .
# create and set non-root USER
RUN addgroup -g 1001 appuser && \
    adduser -S -u 1001 -G appuser appuser
RUN chown -R appuser:appuser /app && \
    chmod 755 /app
USER appuser

EXPOSE 8005
ENTRYPOINT ["/app/entrypoint", "-seedPath=/app/seed_data.sql", "-ip=0.0.0.0", "-port=8005"]

