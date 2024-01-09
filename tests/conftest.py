import os
import sys
from pathlib import Path
from subprocess import run, CompletedProcess
from uuid import uuid4

import docker
import pytest
from docker.models.images import Image
from docker.client import DockerClient
from pytest_cookies.plugin import Result


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    return docker.client.from_env()


@pytest.fixture(scope="session")
def hot_cookie(cookies_session) -> Result:
    result: Result = cookies_session.bake(
        extra_context={
            "project_name": "Test Docker build",
            "project_version": "1.0.0",
            "project_description": "This project is used to test the docker image build process.",
            "author_name": "Max Pfeiffer",
            "author_email": "max@maxpfeiffer.ch",
        }
    )
    return result


@pytest.fixture(scope="session")
def environment_variables(hot_cookie: Result) -> dict:
    # Configuring paths
    virtual_environment_path: Path = hot_cookie.project_path / ".venv"
    virtual_environment_binary_path: Path = virtual_environment_path / "bin"

    # Acquiring system environment variables
    environment_variables: dict = os.environ.copy()

    # "Deactivate" the old and "activate" the new virtual environment: strip the current virtual environment path and
    # add the new virtual environment path.
    # See: https://docs.python.org/3/library/venv.html#how-venvs-work
    if sys.prefix != sys.base_prefix:
        paths: list[str] = environment_variables["PATH"].split(os.pathsep)

        old_virtual_environment_binary_path: str = f"{sys.prefix}/bin"
        cleaned_paths: list[str] = [
            item
            for item in paths
            if item != old_virtual_environment_binary_path
        ]

        cleaned_paths.insert(0, str(virtual_environment_binary_path))
        environment_variables["PATH"] = os.pathsep.join(cleaned_paths)

    # Pointing VIRTUAL_ENV to the new virtual environment
    environment_variables["VIRTUAL_ENV"] = str(virtual_environment_path)

    # Configuring Poetry to put the virtual environment in project directory
    environment_variables["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"

    return environment_variables


@pytest.fixture(scope="session")
def lock_file_context(hot_cookie: Result, environment_variables: dict) -> dict:
    # Create Poetry lock file for building Docker container
    completed_process: CompletedProcess = run(
        ["poetry", "lock"],
        cwd=hot_cookie.project_path,
        env=environment_variables,
    )
    if completed_process.returncode > 0:
        raise Exception("Lock file could not be created with Poetry.")

    return environment_variables


@pytest.fixture(scope="session")
def virtual_environment_context(
    hot_cookie: Result, environment_variables: dict
) -> dict:
    # Install virtual environment with Poetry
    completed_process: CompletedProcess = run(
        ["poetry", "install", "--no-interaction", "--no-root"],
        cwd=hot_cookie.project_path,
        env=environment_variables,
    )
    if completed_process.returncode > 0:
        raise Exception("Virtual environment could not be created with Poetry.")

    return environment_variables


@pytest.fixture(scope="session")
def production_image(
    docker_client: DockerClient, hot_cookie: Result, lock_file_context: dict
) -> str:
    path: str = str(hot_cookie.project_path)
    tag: str = str(uuid4())

    image: Image = docker_client.images.build(
        path=path,
        dockerfile="Dockerfile",
        tag=tag,
        target="production-image",
    )[0]
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="function")
def cleaned_up_test_container(docker_client: DockerClient, request) -> None:
    test_container_name: str = request.param
    yield test_container_name
    test_container = docker_client.containers.get(test_container_name)
    test_container.stop()
    test_container.remove()
