#!/usr/bin/env python3
"""Sync package versions from example-package to template pyproject.toml files."""

import re
import shutil
import sys
from pathlib import Path
from typing import Dict


def parse_pyproject_toml(file_path: Path) -> Dict[str, Dict[str, str]]:
    """Parse pyproject.toml and extract all dependency groups with versions."""
    content = file_path.read_text()

    # Find all dependency groups
    groups = {}

    # Main dependencies (not in a group)
    main_deps_pattern = r"\[tool\.poetry\.dependencies\]\n(.*?)(?=\n\[|\n$)"
    main_match = re.search(main_deps_pattern, content, re.DOTALL)

    if main_match:
        main_content = main_match.group(1)
        main_deps = {}
        for line in main_content.strip().split("\n"):
            line = line.strip()
            if line and "=" in line and not line.startswith("python"):
                package, version = line.split("=", 1)
                main_deps[package.strip()] = version.strip()
        if main_deps:
            groups["dependencies"] = main_deps

    # Find all group dependencies
    group_pattern = (
        r"\[tool\.poetry\.group\.([^\]]+)\.dependencies\]\n(.*?)(?=\n\[|\n$)"
    )
    group_matches = re.finditer(group_pattern, content, re.DOTALL)

    for match in group_matches:
        group_name = match.group(1)
        group_content = match.group(2)
        group_deps = {}

        for line in group_content.strip().split("\n"):
            line = line.strip()
            if line and "=" in line:
                package, version = line.split("=", 1)
                group_deps[package.strip()] = version.strip()

        if group_deps:
            groups[group_name] = group_deps

    return groups


def update_pyproject_toml(
    file_path: Path, new_groups: Dict[str, Dict[str, str]]
) -> None:
    """Update pyproject.toml with new dependency versions for all groups."""
    content = file_path.read_text()

    # Update main dependencies
    if "dependencies" in new_groups:
        for package, version in new_groups["dependencies"].items():
            pattern = rf"({re.escape(package)}\s*=\s*).*"
            replacement = rf"\g<1>{version}"
            content = re.sub(pattern, replacement, content)

    # Update group dependencies
    for group_name, packages in new_groups.items():
        if group_name == "dependencies":
            continue  # Already handled above

        for package, version in packages.items():
            pattern = rf"({re.escape(package)}\s*=\s*).*"
            replacement = rf"\g<1>{version}"
            content = re.sub(pattern, replacement, content)

    file_path.write_text(content)


def sync_lockfile(source_lockfile: Path, target_lockfile: Path) -> None:
    """Copy the lockfile from source to target."""
    if source_lockfile.exists():
        shutil.copy2(source_lockfile, target_lockfile)
        print(f"  Lockfile synced: {target_lockfile}")
    else:
        print(f"  Warning: Source lockfile not found: {source_lockfile}")


def main():
    """Sync versions."""
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

    example_pyproject = example_package_dir / "pyproject.toml"
    template_pyproject = template_dir / "pyproject.toml"
    example_lockfile = example_package_dir / "poetry.lock"

    if not example_pyproject.exists():
        print(f"Error: {example_pyproject} does not exist")
        sys.exit(1)

    if not template_pyproject.exists():
        print(f"Error: {template_pyproject} does not exist")
        sys.exit(1)

    print("Parsing example-package pyproject.toml...")
    example_groups = parse_pyproject_toml(example_pyproject)

    total_packages = sum(len(packages) for packages in example_groups.values())
    print(
        f"Found {len(example_groups)} dependency groups with {total_packages} total "
        "packages"
    )

    print("Updating template pyproject.toml...")
    update_pyproject_toml(template_pyproject, example_groups)

    print("Syncing lockfiles...")
    # Sync template lockfile
    example_lockfile = example_package_dir / "poetry.lock"
    template_lockfile = template_dir / "poetry.lock"
    sync_lockfile(example_lockfile, template_lockfile)

    print("Version sync completed successfully!")

    # Print summary of changes
    for group_name, packages in example_groups.items():
        if packages:
            print(f"\n{group_name.title()} updated:")
            for package, version in packages.items():
                print(f"  {package}: {version}")


if __name__ == "__main__":
    main()
