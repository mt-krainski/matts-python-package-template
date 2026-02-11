# Matt's Python Package Template

[![CI](https://github.com/mt-krainski/matts-python-package-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mt-krainski/matts-python-package-template/actions/workflows/ci.yml)

I recently found myself creating a few packages and copying over the template, so I decided to create a cookie-cutter out of it.

Here's what you get:

- package management with [uv](https://docs.astral.sh/uv/)
- script management with [Poe the Poet](https://poethepoet.natn.io/index.html)
- linting and formatting with [Ruff](https://docs.astral.sh/ruff/)
- a collection of [pre-commit](https://pre-commit.com/) hooks
- GitHub CI with tests, linting, and a template regeneration check
- Dependabot with auto-merge and automatic version synchronization across template files

## Prerequisites

- [pyenv](https://github.com/pyenv/pyenv#installation) for Python version management
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for package management
- [Poe the Poet](https://poethepoet.natn.io/installation.html) for task running
- [pre-commit](https://pre-commit.com/#install) for git hooks
- [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html) for generating packages from this template

## Quick Start

```bash
cookiecutter gh:mt-krainski/matts-python-package-template
cd <your-package>
poe configure
```

Verify everything works:

```bash
poe lint
poe test
```

## Available Tasks

| Task               | Description                                                                      |
| ------------------ | -------------------------------------------------------------------------------- |
| `poe configure`    | Set up the development environment (install deps, pre-commit hooks, `.env` file) |
| `poe update`       | Update dependencies and pre-commit hooks                                         |
| `poe lint`         | Run Ruff linting and format checks                                               |
| `poe test`         | Run tests with coverage and display the coverage report                          |
| `poe hooks-run`    | Run all pre-commit hooks against the repo                                        |
| `poe hooks-update` | Update pre-commit hooks to latest versions                                       |

This list may be incomplete. Check `poe` for a full list of available commands.

## CI

Every push or PR to `main` runs:

1. Tests (`poe test-full`)
2. Linting (`poe lint`)
3. Pre-commit hooks (`poe hooks-run`)

The template repo CI also regenerates `example-package/` from the template and verifies the result matches what's committed. This catches any drift between the template and its example output.

## Repository Setup

To enable Dependabot auto-merge on a generated package, you need two changes in your GitHub repository settings:

1. Create a **Ruleset** for the `main` branch. Enable "Require status checks to pass" with at least the `test` check.
2. Enable **"Allow auto-merge"** under General settings.

## Version Synchronization

This template includes an automated system that keeps package versions in sync between the `example-package/` directory and the template files. Here's how it works:

1. **Dependabot** creates PRs to update dependencies in `example-package/`
2. **Sync workflow** automatically runs on Dependabot PRs (when opened, synchronized, or reopened)
3. **Version sync script** (`poe sync-versions`) updates the dependencies in the template package
4. **Changes are committed** directly to the Dependabot PR with a summary comment

### Manual Sync

You can manually sync versions at any time:

```bash
poe sync-versions
```

This will sync versions from `example-package/` to the template directory and update the lockfile.
