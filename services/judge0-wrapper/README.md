# Judge0 Wrapper

I chose Judge0 because it is a robust code runner.

However, it doesn't support our specific use case of distributing *different* output than program output, i.e. distributing flags.

As such, I've modified the IDE and built an API wrapper to support challenge prompts and distributing flags on the correct answers.

Note that, at this point, only direct matches on output are supported, which should be sufficient.

> See [Judge0's API Documention](https://ce.judge0.com/), for reference.

The only endpoint we modify is `/submissions`, to add a "flag" key and value. It defaults to `""` when the output does not match the expected result. Everything else is just passed along.

We also add a `/challenge_info/{:id}` endpoint, which takes a challenge number and returns the prompt and expected output.

TODO: Deploy with pm2

