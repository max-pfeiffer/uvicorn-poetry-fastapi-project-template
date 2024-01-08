import os
from pathlib import Path
from subprocess import run, CompletedProcess

from pytest_cookies.plugin import Result


def configure_environment_variables(hot_cookie: Result) -> dict:
    # Configuring paths
    virtual_environment_path: Path = hot_cookie.project_path / ".venv"
    virtual_environment_binary_path: Path = virtual_environment_path / "bin"

    # Acquiring system environment variables
    environment_variables = os.environ.copy()

    # Setting the environment variable pointing to the new virtual environment
    environment_variables["VIRTUAL_ENV"] = str(virtual_environment_path)
    environment_variables["PATH"] += os.pathsep + str(
        virtual_environment_binary_path
    )

    return environment_variables


def setup_lock_file(hot_cookie: Result) -> dict:
    environment_variables: dict = configure_environment_variables(hot_cookie)

    # Create Poetry lock file for building Docker container
    completed_process: CompletedProcess = run(
        ["poetry", "lock"],
        cwd=hot_cookie.project_path,
        env=environment_variables,
    )
    if completed_process.returncode > 0:
        raise Exception("Lock file could not be created with Poetry.")

    return environment_variables


def setup_virtual_environment(hot_cookie: Result) -> dict:
    environment_variables: dict = configure_environment_variables(hot_cookie)

    # Install virtual environment with Poetry
    completed_process: CompletedProcess = run(
        ["poetry", "install", "--no-interaction", "--no-root"],
        cwd=hot_cookie.project_path,
        env=environment_variables,
    )
    if completed_process.returncode > 0:
        raise Exception("Virtual environment could not be created with Poetry.")

    return environment_variables
