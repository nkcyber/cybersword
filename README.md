# NKCyber Cybersword

Themed Description:

> Join Barty the Cyber Knight as he tries to earn the mystical CyberSword through a series of fun online challenges! This competition is intended for students who are looking to have a hands-on experience with Python programming, hacking, and cybersecurity. Students will need a laptop or desktop machine with an updated browser and an internet connection.

Neutral Description:

> CyberSword is a friendly, online cybersecurity competition for high schoolers. Students will complete a series of fun challenges and gain hands-on experience with Python programming, SQL, and cybersecurity. Students will need a laptop or desktop machine with an updated browser and an internet connection.

## Getting Started

> [!IMPORTANT]
> This repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
> Remember to clone with `--recursive`:
> ```bash
> git clone git@github.com:nkcyber/cybersword.git --recursive
> ```

To get started with this project, install the [CTFd CLI](https://github.com/CTFd/ctfcli) and run `ctf init` to initalze your project information.

See [`administration.md`](./docs/administration.md) for more information.

## About
This project uses the [CTFd CLI](https://github.com/CTFd/ctfcli) for challenge management.

## Resources

Check [the documentation](https://github.com/nkcyber/cybersword/tree/main/docs) for more information about running this event.

## Service Deployment

Note that [automatic challenge deployment](https://docs.ctfd.io/tutorials/challenges/deploying-challenges/#automatic-challenge-deployment-service) is not available in the free version, which we're using.

As such, we have to take a more involved approach to challenge service deployment.

-------

<details>

<summary>TO DO</summary>

- Important:
    - Fix bad user experience with AI lab
    - Modify installation script to support cgroups configuration
    - Write test suite to check that ai lab & code runner are set up correctly
- Services:
    - how to sync files and images in CTFd?
        - use nkcyber logo in index page and whatnot
    - create introduction page in CTFd explaining goals and how to submit flags.
- Create challenges:
    - [3d call to action](https://www.youtube.com/watch?v=x3m1PGEfG5c) - Barty needs your help!
	- Sensitive Data Exposure: API backend
	- API you can manipulate (access=false)
	- encryption method that's not an encryption method
	- IDOR
    - flag commented out in webpage
    - developer tools
    - Teach web exploits:
        - https://owasp.org/Top10/A01_2021-Broken_Access_Control/
        - Automatically Incrementing IDs in URL allowing to resource discovery
    - how to teach binary decompilation in a browser?
    - embed a flag in a JWT (easy to make!)
    - teach people that PDFs can phone home
    - how to teach buffer overflow in a browser?
    - how to teach timing attack in a browser?
        - use judge0 scripting environment
        - prerequisite: binary search in python

- Story:
    - this has been dropped for practical reasons.
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

</details>

----

## Timing information

See [`docs/timing.md`](./docs/timing.md).

