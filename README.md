# Matt's Python Package Template

[![CI](https://github.com/mt-krainski/matts-python-package-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mt-krainski/matts-python-package-template/actions/workflows/ci.yml)
[![Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg)](https://cookiecutter.readthedocs.io/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A batteries-included [Cookiecutter](https://cookiecutter.readthedocs.io/) template for modern Python packages — with **uv**, **Ruff**, **pre-commit**, **CI**, and **Dependabot** baked in.

## Features

- **Package management** — [uv](https://docs.astral.sh/uv/) for fast, reliable dependency resolution
- **Task runner** — [Poe the Poet](https://poethepoet.natn.io/index.html) for simple, cross-platform task definitions
- **Linting & formatting** — [Ruff](https://docs.astral.sh/ruff/) with a curated set of lint rules
- **Git hooks** — [pre-commit](https://pre-commit.com/) with hooks for linting, formatting, and more
- **CI** — GitHub Actions workflow for tests, linting, and hook checks out of the box
- **Dependency updates** — Dependabot configuration with auto-merge support

## Quick Start

### Prerequisites

- [pyenv](https://github.com/pyenv/pyenv#installation) for Python version management
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for package management
- [Poe the Poet](https://poethepoet.natn.io/installation.html) for task running
- [pre-commit](https://pre-commit.com/#install) for git hooks
- [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html) for generating packages from this template

### Generate a new project

```bash
cookiecutter gh:mt-krainski/matts-python-package-template
```

You'll be prompted for a few details:

```
project_name [...]: My Awesome Package
author [...]: Your Name
email [...]: you@example.com
use_jupyter [y]: n
```

Then set up your development environment:

```bash
cd my-awesome-package
poe configure
```

This installs dependencies, sets up pre-commit hooks, and creates a `.env` file.

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

Run `poe` with no arguments for a full list of available tasks.

## CI

Every push or PR to `main` runs:

1. **Tests** (`poe test-full`)
2. **Linting** (`poe lint`)
3. **Pre-commit hooks** (`poe hooks-run`)

## Design Decisions

This template is opinionated — it picks modern, fast tooling and prioritizes a single-tool-per-job approach.

- **uv** — Written in Rust, blazing fast, and consolidates package management, virtualenv creation, and Python version management into a single binary. Quickly becoming the de facto standard for modern Python projects.
- **Ruff** — A single tool for both linting and formatting, with 800+ built-in rules that run in under a second. Adopted by FastAPI, Pandas, Airflow, and many others.
- **Poe the Poet** — Tasks defined directly in `pyproject.toml`, automatic virtual environment integration, and support for sequences, arguments, and shell completion. Think npm scripts, but for Python.

<details>
<summary><h2>Template Maintenance</h2></summary>

### Template CI

The template repo CI also regenerates `example-package/` from the template and verifies the result matches what's committed. This catches any drift between the template and its example output.

### Repository Setup

To enable Dependabot auto-merge on a generated package, you need two changes in your GitHub repository settings:

1. Create a **Ruleset** for the `main` branch. Enable "Require status checks to pass" with at least the `test` check.
2. Enable **"Allow auto-merge"** under General settings.

### Version Synchronization

This template includes an automated system that keeps package versions in sync between the `example-package/` directory and the template files. Here's how it works:

1. **Dependabot** creates PRs to update dependencies in `example-package/`
2. **Sync workflow** automatically runs on Dependabot PRs (when opened, synchronized, or reopened)
3. **Version sync script** (`poe sync-versions`) updates the dependencies in the template package
4. **Changes are committed** directly to the Dependabot PR with a summary comment

You can manually sync versions at any time:

```bash
poe sync-versions
```

This will sync versions from `example-package/` to the template directory and update the lockfile.

</details>

## Contributing

Contributions are welcome — feel free to open an issue or submit a PR.

## License

This project is licensed under the [MIT License](LICENSE).
