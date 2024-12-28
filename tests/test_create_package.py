import os
import shutil
import subprocess  # noqa: S404

from cookiecutter.main import cookiecutter


def _try_subprocess(*args, **kwargs):
    result = subprocess.run(*args, **kwargs)  # noqa: S603
    result.check_returncode()


def test_create_package():
    """Create a new package from template and run basic checks."""
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

    _try_subprocess(["poe", "configure"], cwd="test-package")
    _try_subprocess(["poe", "lint"], cwd="test-package")
    _try_subprocess(["poe", "test"], cwd="test-package")

    shutil.rmtree("test-package")
