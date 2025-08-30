# Matt's Python Package Template

I recently found myself creating a few packages and copying over the template, so I decided to create a cookie-cutter out of it.

Here's what you get:

- package management with [Poetry](https://python-poetry.org/)
- script management with [Poe the Poet](https://poethepoet.natn.io/index.html)
- code formatting with [Black](https://black.readthedocs.io/en/stable) and [isort](https://pycqa.github.io/isort/)
- pretty solid set of flake8 linters
- a collection of [pre-commit](https://pre-commit.com/) hooks
- GitHub CI that will install, test, and lint your package on every PR or push to main
- basic Dependabot configuration, including auto-approving PRs if tests pass. This requires a few changes to Github repository Settings:
  1. Create a "Ruleset" for the main branch. "Require status checks to pass", with at least the "test" step.
  2. "Allow auto-merge" under "General" settings.
- Automatic version synchronization from `example-package/` to template files after Dependabot updates

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
