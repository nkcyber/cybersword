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

```bash
# stop firewall on Fedora 39
sudo systemctl stop firewalld
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

## Regularly remove garbage docker containers

Despite being run with `--rm`, it looks like the webshell challenges create some cruft that uses up disk space over time.

This can be addressed with a cronjob like:

```cron
0 0 * * 0 docker system prune -a -f
```

to automatically clean all unused docker images every Sunday.

Note that we actually want the docker images to sit around for a little bit, just so that they're cached and ready to go for other competitors.

## Pre-caching webshell challenges

If you are about to run the webshell challenges, it can be nice to ensure they're all cached for the competitors.

You can run a script like this:

```
for i in {1..6}; do xdg-open "https://ctf.nkcyber.org/webshell-$i/"; done
```

To open all of the URLs in your browser.

(Or you could do this manually, or not at all.)

The benefit of doing this is that the first people loading the challenges do not have to wait for the container to build from scratch.

## Troubleshooting

### Judge0 cgroups settings

If you get an error with judge0 that "chown: cannot access '/box': No such file or directory", you may need to follow this advice:
<https://github.com/judge0/judge0/issues/325#issuecomment-1429381789>

```bash
sudo nano /etc/default/grub
# edit this line, and save:
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
sudo update-grub
sudo reboot
```

#### Fedora solution

Note, it used to be:
```bash
GRUB_CMDLINE_LINUX="rhgb quiet"
```

And I changed it to
```bash
GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=0"
```
and ran on Fedora:
```bash
sudo grub2-mkconfig -o "$(readlink -e /etc/grub2.conf)"
sudo reboot
```

### Errors in ropchain lab

If you get errors like this in the ropchain lab:

![image](https://github.com/user-attachments/assets/b9951c4e-e3dd-4a0d-965c-21951cf74ef6)

It means you need to run this script from the ropchain labs:

- <https://github.com/nkcyber/ropchain-lab/blob/main/setup-host.sh>

### Hack to get Ollama working

![image](https://github.com/nkcyber/cybersword/assets/46602241/50e91aa8-bbdd-4caa-a0ad-8f029d804b41)

I really dislike Ollama's two part setup that doesn't fit in docker compose.

As of 2024-01-31, I was able to run:

```bash
docker compose exec ollama sh
```
and then inside
```bash
bash # to upgrade from sh to bash
ollama pull tinyllama # to install the model
```

I'm actively looking into ways to make this just part of docker compose.

### CTFd doesn't start up immediately

A few times during development today (2024-03-11), I've encountered an issue where CTFd fails to start up.

```
nginx-1                  | 2024/03/11 15:03:22 [emerg] 1#1: host not found in upstream "ctfd:8000" in /etc/nginx/upstreams.conf:3
nginx-1                  | nginx: [emerg] host not found in upstream "ctfd:8000" in /etc/nginx/upstreams.conf:3
nginx-1 exited with code 0
```

This feels like a race condition between the nginx and ctfd docker images, but I'm not sure.

Either way, I was able to resolve the issue by just running `docker compose down && docker compose up --build` again.

Potential solutions may include [controlling startup order](https://docs.docker.com/compose/startup-order/) in docker.

