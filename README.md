# NKCyber Cybersword

Join Barty the Cyber Knight as he tries to earn the mystical CyberSword through a series of fun online challenges! This competition is intended for students who are looking to have a hands-on experience with Python programming, hacking, and cybersecurity.

## Getting Started

> [!IMPORTANT]
> This repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
> Remember to clone with `--recursive`:
> ```bash
> git clone git@github.com:nkcyber/cybersword.git --recursive
> ```

To run the services and CTFd, run:

```
docker compose down && docker compose build && docker compose up
```

To get started with this project, install the [CTFd CLI](https://github.com/CTFd/ctfcli) and run `ctf init` to initalze your project information.

See [`administration.md`](./docs/administration.md) for more information.

## Important Dates

We hope to use this project *at least* at the following events.

### TSA
**February 9th, 2024**

Technology Student Association (TSA)
Open to students enrolled in or who have completed technology and education courses, TSA’s membership includes more than 300,000 middle and high school students across the United States.

### TechOlympics
**February 17-18th, 2024**

https://www.techolympics.org/

Procter and Gamble Global Headquarters ([13 min drive](<https://maps.app.goo.gl/F9oLckWUZ9r1gavx6>))

### STLP24 State Championship
**March 27th, 2024** ([Link to important dates](<https://docs.google.com/spreadsheets/d/e/2PACX-1vRD4ewagNee3_hIkydpecvRcqDvCveMy5BcG0z_zYb97jKAf49fmfy6pHd5fPiUUkjVrJo3SmacYRka/pubhtml#:~:text=3/27,Championship%20%2D%20Lexington%2C%20KY>))

**Rupp Arena**, Lexington Kentucky ([1 hr drive south](<https://maps.app.goo.gl/rkJ678c678UKmuZ56>))

## About
This project uses the [CTFd CLI](https://github.com/CTFd/ctfcli) for challenge management.

## Resources

### Examples of other CTFs using CTFd CLI

Look through these for examples on how to configure challenges deployed with Docker:

- <https://github.com/BreizhCTF/breizhctf-2023>
- <https://github.com/echoCTF/echoCTF.RED>
- <https://github.com/DragonSecSI/DCTF-2022>
- <https://github.com/HeroCTF/HeroCTF_v4?>
- <https://github.com/issessions/ISSessionsCTF2022>
- <https://github.com/adventofctf/2020>
- <https://github.com/CTF-Inter-IUT/InterIUT-2020>
- <https://github.com/les-amateurs/AmateursCTF-Public>
- <https://github.com/ESAIP-CTF/public-esaip-ctf-2023>

We can also use [the built in templates](https://docs.ctfd.io/docs/management/ctfcli/templates/).

## Service Deployment

Note that [automatic challenge deployment](https://docs.ctfd.io/tutorials/challenges/deploying-challenges/#automatic-challenge-deployment-service) is not available in the free version, which we're using.

As such, we have to take a more involved approach to challenge service deployment.

-------

To Do:
- Figure out how to host CTFd and several challenges all on the same server
    - NGINX reverse proxy
        - https://gcore.com/learning/reverse-proxy-with-docker-compose/
    - CTFd as a git subrepo?
- Clone structure of <https://github.com/adventofctf/2020/tree/main>
    - Then, set up github integration to update deployed version to latest git repo
- Create challenges:
    - [3d call to action](https://www.youtube.com/watch?v=x3m1PGEfG5c) - Barty needs your help!
    - Data commented out in webpage
    - developer tools
    - using code submissions for flags
        - Judge0 versus CTFd code submissions?
    - Teach Python:
        - variables
        - if statements
        - for loops
        - `with` connections for networks
        - establish a network connection to a service with pwntools, send it input, and then do something fun with the result
        - takeaway: know that you can use python to automate connection processing
- Story:
    - We are writing an [excuse plot](https://tvtropes.org/pmwiki/pmwiki.php/Main/ExcusePlot)
        - [So you want to write an excuse plot (advice)](https://tvtropes.org/pmwiki/pmwiki.php/SoYouWantTo/WriteAnExcusePlot)
    - Where did barty come from?
    - **Key point:** Because we did the "CyberShield" compeition in the past. We're doing the CyberSword competition now.
        - What's the lore for the CyberSword
            - It's a sign of cybersecurity proficiency.
    - Why do we have to complete challenges to earn the cyber sword?
    - Things that the story should have:
        - I like the idea of a mideval knight not knowing anything about cybersecurity.
            - Therefore, the user has to support him in his efforts.
        - I like the idea of a mideval knight just wandering around northern kentucky.


State clear goal in "bookends" for each subject:
    - You don't have to know anything now
    - When you're done, you'll either win or know what you don't know
