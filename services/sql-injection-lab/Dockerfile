# modified from https://github.com/a-h/templ/blob/main/examples/counter-basic/Dockerfile

# TODO: create seed data derived from challenge flags

# Build.
FROM golang:alpine3.19 AS build-stage
RUN apk add --no-cache \
    # Important: required for go-sqlite3
    gcc \
    # Required for Alpine
    musl-dev
WORKDIR /app
COPY sql-injection-lab /app
RUN go mod download
RUN CGO_ENABLED=1 GOOS=linux go build -C /app -o /entrypoint
COPY seed_data.sql /seed_data.sql

# Deploy as non-root user
FROM golang:alpine3.19 AS release-stage
WORKDIR /app
COPY seed_data.sql .
COPY --from=build-stage /entrypoint .
# create and set non-root USER
RUN addgroup -g 1001 appuser && \
    adduser -S -u 1001 -G appuser appuser
RUN chown -R appuser:appuser /app && \
    chmod 755 /app
USER appuser

EXPOSE 8005
ENTRYPOINT ["/app/entrypoint", "-seedPath=/app/seed_data.sql", "-ip=0.0.0.0", "-port=8005"]

