import os
import shutil
import subprocess

from cookiecutter.main import cookiecutter


def try_subprocess(*args, **kwargs):
    result = subprocess.run(*args, **kwargs)
    result.check_returncode()


def test_create_package():
    if os.path.exists("test-package"):
        shutil.rmtree("test-package")

    cookiecutter(
        ".",
        no_input=True,
        extra_context={
            "project_name": "Test Package",
            "author": "Test User",
            "email": "test@test.com",
        },
    )

    assert os.path.isdir("test-package")
    assert os.path.exists("test-package/pyproject.toml")

    try_subprocess(["poe", "configure"], cwd="test-package")
    try_subprocess(["poe", "lint"], cwd="test-package")
    try_subprocess(["poe", "test"], cwd="test-package")

    shutil.rmtree("test-package")
