# Administration

## Installing

### Install Locally

#### Clone Project

> [!IMPORTANT]
> This repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
>
> Remember to clone with `--recursive`:
> ```bash
> git clone git@github.com:nkcyber/cybersword.git --recursive
> ```

#### Install Docker and Docker Compose

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

This project requires Docker Compose >= 2.21

#### Install CTFd CLI

- [Install CTFd CLI](https://github.com/CTFd/ctfcli?tab=readme-ov-file#installation-and-usage)

### Setup on Digital Ocean droplet

To automatically clone the repo and set up Docker, copy [`set_up_cybersword.sh`](../scripts/set_up_cybersword.sh) to your droplet:

```bash
# NAVIGATE TO cybersword DIRECTORY
YOUR_SERVER="" # put your server name here
# create directory
ssh root@$YOUR_SERVER "mkdir -p /root/nkcyber"
# copy script to server
scp ./scripts/set_up_cybersword.sh root@$YOUR_SERVER:/root/nkcyber
# ssh into the server...
ssh root@$YOUR_SERVER
```
After ssh-ing into the server:
```bash
cd "/root/nkcyber/"
# install project files & docker
./set_up_cybersword.sh
sudo reboot
```

## Administration / Running services

> [!NOTE]
> Adding `-d` or `--detach` to any `docker compose up` command will make it run in the background, which may be useful when deploying on a server.

### Run with http

[`docker-compose.yml`](../docker-compose.yml) contains the configurations to deploy an http service, primarily used for development.

```bash
# in cybersword directory
docker compose down && docker compose up --build
```

### Run with https

[`docker-compose.https.yml`](../docker-compose.https.yml) contains the configurations to deploy an http**s** service, intended for production.

Use [`set_up_https.sh`](../scripts/set_up_https.sh) to set up http certs on your server prior to using this command.

```bash
# in cybersword directory
docker compose down && docker compose -f docker-compose.https.yml down && docker compose -f docker-compose.https.yml up --build
```

## Challenge Management

This project uses the [CTFd CLI](https://github.com/CTFd/ctfcli) for challenge management.

### Install all challenges on a new server

```bash
# cd into CyberSword directory
./scripts/add_all_challenges.sh
ctf challenge install
ctf challenge sync
ctf pages push
```

It's necessary to install then sync because challenges are created in alphabetical order, and they cannot depend on a challenge that doesn't exist yet.
Rather than trying to organize everything in order of dependencies (which may change), I think it's best to just run this two phase setup.

(you can also use `./scripts/install_all_challenges.sh`, or ``./scripts/sync_all_challenges.sh``).

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

You might need to allow port 80 on your firewall if things are not deploying correctly.

```
# stop firewall on Fedora 39
sudo systemctl stop firewalld
```



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
and ran on Fedora:
```
sudo grub2-mkconfig -o "$(readlink -e /etc/grub2.conf)"
```


## Remove broken "share" button from all challenges.

If you don't want the share button to be on all the challenges, go to <http://localhost/admin/config>, under the tab "Theme" and header "Theme Header", and add the HTML:

```html
<style>
button[x-show="!share_url"] {
    display: none;
}
</style>
```

and click "Update".


