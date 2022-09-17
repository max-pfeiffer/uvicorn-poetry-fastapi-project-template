from subprocess import run, CompletedProcess
from uuid import uuid4

import docker
import pytest
from docker.models.images import Image
from pytest_cookies.plugin import Result


@pytest.fixture(scope="session")
def docker_client() -> docker.client:
    return docker.client.from_env()


@pytest.fixture(scope="session")
def docker_file_name() -> str:
    return "Dockerfile"


@pytest.fixture(scope="session")
def docker_image_test_project(cookies_session):
    result: Result = cookies_session.bake(
        extra_context={
            "project_name": "Test Docker build",
            "project_version": "1.0.0",
            "project_description": "This project is used to test the docker image build process.",
            "author_name": "Max Pfeiffer",
            "author_email": "max@maxpfeiffer.ch",
        }
    )

    # Install project dependencies with Poetry
    completed_process: CompletedProcess = run(
        ["poetry", "install"], cwd=result.project_path
    )
    if completed_process.returncode > 0:
        raise Exception("Dependencies were not installed with Poetry.")

    return result


@pytest.fixture(scope="session")
def production_image(
    docker_client, docker_image_test_project, docker_file_name
) -> str:
    path: str = str(docker_image_test_project.project_path)
    tag: str = str(uuid4())

    image: Image = docker_client.images.build(
        path=path,
        dockerfile=docker_file_name,
        tag=tag,
        target="production-image",
    )[0]
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="session")
def development_image(
    docker_client, docker_image_test_project, docker_file_name
) -> str:
    path: str = str(docker_image_test_project.project_path)
    tag: str = str(uuid4())

    image: Image = docker_client.images.build(
        path=path,
        dockerfile=docker_file_name,
        tag=tag,
        target="development-image",
    )[0]
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="session")
def black_test_image(
    docker_client, docker_image_test_project, docker_file_name
) -> str:
    path: str = str(docker_image_test_project.project_path)
    tag: str = str(uuid4())

    image: Image = docker_client.images.build(
        path=path,
        dockerfile=docker_file_name,
        tag=tag,
        target="black-test-image",
    )[0]
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="session")
def test_image(
    docker_client, docker_image_test_project, docker_file_name
) -> str:
    path: str = str(docker_image_test_project.project_path)
    tag: str = str(uuid4())

    image: Image = docker_client.images.build(
        path=path,
        dockerfile=docker_file_name,
        tag=tag,
        target="test-image",
    )[0]
    image_tag: str = image.tags[0]
    yield image_tag
    docker_client.images.remove(image_tag, force=True)


@pytest.fixture(scope="function")
def cleaned_up_test_container(docker_client, request) -> None:
    test_container_name: str = request.param
    yield test_container_name
    test_container = docker_client.containers.get(test_container_name)
    test_container.stop()
    test_container.remove()
