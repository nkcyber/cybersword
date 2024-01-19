# Judge0 IDE

This is modified from https://github.com/judge0/ide

Their code is built in a way that it's difficult to host without directly modifying the code.

It has been modified to:
- parse challenge ids from url fragments ("#challenge=123")
- show an interactive tour when the challenge id equals `0`.
- show challenge prompts, input, and expected output from the [`judge0-wrapper`](../judge0-wrapper/)
- show the flag when returned from [`judge0-wrapper`](../judge0-wrapper/)

When starting this server for development, do so in this directory.

The editor must be mounted at `/ide/index.html`

If you're running this with `docker compose`, and you modify `challenges.yml`, you must reload everything for your changes to take effect. This is because challenges.yml is run once at program start, and the results are cached for subsequent uses. More intelligent caching would resolve this, but `docker compose down && docker compose up --build` should do the trick.

