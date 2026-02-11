#!/usr/bin/env python3
"""Sync package versions from example-package to template pyproject.toml files."""

import re
import shutil
import sys
import tomllib
from pathlib import Path
from typing import Dict


def parse_dependency_name(dep_string: str) -> str | None:
    """Extract package name from a PEP 508 dependency string."""
    match = re.match(r"^([a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?)", dep_string)
    if match:
        return match.group(1)
    return None


def parse_dependencies(pyproject_path: Path) -> Dict[str, Dict[str, str]]:
    """Parse all dependencies from a pyproject.toml file.

    Returns a dict of {group_name: {package_name: full_dep_string}}.
    """
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    groups: Dict[str, Dict[str, str]] = {}

    # Parse project dependencies
    project_deps = data.get("project", {}).get("dependencies", [])
    for dep in project_deps:
        name = parse_dependency_name(dep)
        if name:
            groups.setdefault("dependencies", {})[name] = dep

    # Parse dependency groups
    dep_groups = data.get("dependency-groups", {})
    for group_name, group_deps in dep_groups.items():
        for dep in group_deps:
            if isinstance(dep, str):
                name = parse_dependency_name(dep)
                if name:
                    groups.setdefault(group_name, {})[name] = dep

    return groups


def update_pyproject_toml(
    file_path: Path, source_groups: Dict[str, Dict[str, str]]
) -> None:
    """Update dependency versions in a pyproject.toml file."""
    content = file_path.read_text()

    for packages in source_groups.values():
        for name, full_spec in packages.items():
            # Match only PEP 508 dependency strings with version operators,
            # e.g. "pytest>=9.0.2", not "pytest --showlocals"
            pattern = rf'"{re.escape(name)}(\[[^\]]*\])?\s*(>=|<=|==|~=|!=|>|<)[^"]*"'
            replacement = f'"{full_spec}"'
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

    if not example_pyproject.exists():
        print(f"Error: {example_pyproject} does not exist")
        sys.exit(1)

    if not template_pyproject.exists():
        print(f"Error: {template_pyproject} does not exist")
        sys.exit(1)

    print("Parsing example-package pyproject.toml...")
    example_groups = parse_dependencies(example_pyproject)

    total_packages = sum(len(packages) for packages in example_groups.values())
    print(
        f"Found {len(example_groups)} dependency groups with {total_packages} total "
        "packages"
    )

    print("Updating template pyproject.toml...")
    update_pyproject_toml(template_pyproject, example_groups)

    print("Syncing lockfiles...")
    sync_lockfile(
        example_package_dir / "uv.lock",
        template_dir / "uv.lock",
    )

    print("Version sync completed successfully!")

    # Print summary of changes
    for group_name, packages in example_groups.items():
        if packages:
            print(f"\n{group_name.title()} updated:")
            for name, spec in packages.items():
                print(f"  {name}: {spec}")


if __name__ == "__main__":
    main()
