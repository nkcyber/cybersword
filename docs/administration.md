# Administration

## Installing

TODO
- Clone github repo
- `docker compose up -d`
- run script to install selected challenges

## Project Structure

Note that there are a lot of advanced features like running docker containers and code submissions that are locked behind a paywall for CTFd.

As such, if we want to use CTFd, we basically need to wrap it in an outer shell that adds these extra features.

As such, we have an outer `docker-compose.yml` that orchestrates all of the services.
All services should run under a single docker-compose process exposed on the same port, to make deployment simpler.

From there, `services` contains all of the services that the challenges depend on.

`challenges` simply contains the information that needs to be synced with CTFd.


