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

## Initalize Challenge in CTFd

TODO: clean this up

```
$ docker compose up -d
$ ctf init
Please enter CTFd instance URL: http://localhost
Please enter CTFd Admin Access Token: ctfd_TOKEN
Do you want to continue with http://localhost and ctfd_TOKEN [Y/n]: y
Already in a git repo. Skipping git init.
The following paths are ignored by one of your .gitignore files:
.ctf
$ ctf challenge install challenges/sql/basic_injection
```

Note that changing a flag in a challenge generally warrants rebuilding the application, to ensure that the services register the new flag.

To rebuild the application, do:

```bash
docker compose down
docker compose build
docker compose up -d
```

everything is configured to run on http port 80 right now. (https needs to be added later)

you might need to allow port 80 on your firewall if things are not deploying correctly.

## Troubleshooting

If you get an error with judge0 that "chown: cannot access '/box': No such file or directory", you may need to follow this advice:
    - <https://github.com/judge0/judge0/issues/325#issuecomment-1429381789>

Note, it used to be:
```
GRUB_CMDLINE_LINUX="rhgb quiet"
```

And I changed it to
```
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
```



