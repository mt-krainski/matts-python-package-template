# Matt's Python Package Template

I recently found myself creating a few packages and copying over the template, so I decided to create a cookie-cutter out of it.

Here's what you get:

- package management with [Poetry](https://python-poetry.org/)
- script management with [Poe the Poet](https://poethepoet.natn.io/index.html)
- code formatting with [Black](https://black.readthedocs.io/en/stable)
- pretty solid set of flake8 linters
- a collection of [pre-commit](https://pre-commit.com/) hooks
- GitHub CI that will install, test, and lint your package on every PR or push to main
- basic Dependabot configuration, including auto-approving PRs if tests pass (TODO: this needs additional configuration)
- ChatGPT-based code reviews with `freeedcom/ai-codereviewer` (TODO: replace with my own fork that allows for more configuration)
