#!/usr/bin/env python3
"""Sync pre-commit config versions from example-package to template."""

import re
import sys
from pathlib import Path
from typing import Dict


def parse_precommit_config(file_path: Path) -> Dict[str, str]:
    """Parse .pre-commit-config.yaml and extract repo URLs and their versions."""
    content = file_path.read_text()

    # Find all repo entries with their rev (version) values
    repo_pattern = r"repo:\s*(https://[^\s]+).*?\n\s*rev:\s*([^\s]+)"
    matches = re.finditer(repo_pattern, content, re.DOTALL)

    repo_versions = {}
    for match in matches:
        repo_url = match.group(1)
        version = match.group(2)
        repo_versions[repo_url] = version

    return repo_versions


def update_precommit_config(file_path: Path, new_versions: Dict[str, str]) -> None:
    """Update .pre-commit-config.yaml with new version numbers."""
    content = file_path.read_text()

    # Update each repo version
    for repo_url, new_version in new_versions.items():
        # Find the repo section and update its rev
        pattern = rf"(repo:\s*{re.escape(repo_url)}.*?\n\s*rev:\s*)[^\s]+"
        replacement = rf"\g<1>{new_version}"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    file_path.write_text(content)


def main():
    """Main function to sync pre-commit config versions."""
    root_dir = Path(__file__).parent.parent
    example_package_dir = root_dir / "example-package"
    template_dir = root_dir / "{{ cookiecutter.project_slug }}"

    # Check if directories exist
    if not example_package_dir.exists():
        print(f"Error: {example_package_dir} does not exist")
        sys.exit(1)

    if not template_dir.exists():
        print(f"Error: {template_dir} does not exist")
        sys.exit(1)

    example_precommit = example_package_dir / ".pre-commit-config.yaml"
    template_precommit = template_dir / ".pre-commit-config.yaml"

    if not example_precommit.exists():
        print(f"Error: {example_precommit} does not exist")
        sys.exit(1)

    if not template_precommit.exists():
        print(f"Error: {template_precommit} does not exist")
        sys.exit(1)

    print("Parsing example-package .pre-commit-config.yaml...")
    example_precommit_versions = parse_precommit_config(example_precommit)

    print(f"Found {len(example_precommit_versions)} pre-commit repos to sync")

    print("Updating template .pre-commit-config.yaml...")
    update_precommit_config(template_precommit, example_precommit_versions)

    print("Pre-commit config sync completed successfully!")

    # Print summary of changes
    if example_precommit_versions:
        print("\nPre-commit repos updated:")
        for repo_url, version in example_precommit_versions.items():
            # Extract repo name from URL for cleaner output
            repo_name = repo_url.split("/")[-1]
            print(f"  {repo_name}: {version}")


if __name__ == "__main__":
    main()
