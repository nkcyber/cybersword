# Dependencies

It's important that this project is easy to deploy and maintain.
As such, an effort has been made to document all of the services that are/will be used in this project.

Note that this does not include the complete dependency tree, but just the core dependencies for this project.

| Software          | License                                                                                        |  Commercial Use | Notes                                               |
|-------------------|------------------------------------------------------------------------------------------------|:---------------:|-----------------------------------------------------|
| CTFd software     | [Apache License](https://github.com/CTFd/CTFd/blob/master/LICENSE)                             |        ✅        | This is the strongest dependency for this project. |
| CTFd CLI          | [Apache License](https://github.com/CTFd/ctfcli/blob/master/LICENSE)                           |        ✅        |                                                    |
| CTFd paid hosting | [Terms of Service](https://ctfd.io/terms-of-use/)                                              | ⚠️ With approval | I think CTFd paid hosting is overpriced, and that it'd be more maintainable if we host it ourselves. **We've considered this, but we're not using this.** |
| SQL Injection Lab | [MIT License](https://github.com/nkcyber/sql-injection-lab/blob/main/LICENSE)                  |        ✅        | Developed by Zack Sargent                          |
| Judge0            | [GNU General Public License v3.0](https://github.com/judge0/judge0/blob/master/LICENSE)        |        ✅        | For interactive code evaluation and judging. While GPLv3 requires derivative works to be licensed under a GPLv3 license, I think we're exempt by the [SaaS/ASP](https://www.revenera.com/blog/software-composition-analysis/understanding-the-saas-loophole-in-gpl/) loophole. Idk. I'm not a lawyer. I don't want to make all of the source code publically accesible, because then people could just copy-paste the flags from the challenge.yml files. If we ever have a lawyer take a look at this, this is the main thing that we need to think about. |
| Judge0 IDE        | [MIT License](https://github.com/judge0/ide/blob/master/LICENSE)                               |        ✅        | For interactive code evaluation and judging. This has been copied and modified to work as part of a CTF platform. |
| React             | [MIT License](https://github.com/facebook/react/blob/main/LICENSE)                             |        ✅        |                                                    |
| Docker            | [Apache License 2.0](https://docs.docker.com/engine/#licensing)                                |        ✅        |                                                    |
| Python 3.12       | [PSF License](https://docs.python.org/3/license.html#psf-license-agreement-for-python-release) |        ✅        |                                                    |
| Go                | [BSD 3-Clause "New" or "Revised" License](https://github.com/golang/go/blob/master/LICENSE)    |        ✅        |                                                    |
| Bash              | [GNU General Public License](https://www.gnu.org/software/bash/#license)                       |        ✅        |                                                    |

