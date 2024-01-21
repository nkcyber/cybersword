# Judge0 Wrapper

> [!IMPORTANT]
> All challenges accessible through Judge0 must be configured in  [`challenges.yml`](./challenges.yml).

## About

I chose [Judge0](https://judge0.com/) because it is a robust code runner.

However, it doesn't support our specific use case of distributing *different* output than program output, i.e. distributing flags.

As such, I've modified the IDE and built an API wrapper to support challenge prompts and distributing flags on the correct answers.

Note that, at this point, only direct matches on output are supported, which should be sufficient.

> See [Judge0's API Documention](https://ce.judge0.com/), for reference.

The only endpoint we modify is `/submissions`, to add a "flag" key and value. The flag defaults to `""` when the output does not match the expected result. 
All other api information is left untouched.

We also add a `/challenge_info/{:id}` endpoint, which takes a challenge id and returns information about it.
Our custom Judge0 IDE depends on this endpoint.

## Running

Run locally with `yarn start`. 

Deploy to production with `pm2-runtime index.js` (as seen in the [`Dockerfile`](./Dockerfile)).

For the mot part, everything should be automatically handled by running `docker compose` in the root directory of CyberSword.

