from uuid import uuid4

import docker
import pytest
from docker.models.images import Image
from pytest_cookies.plugin import Result

from tests.utils import setup_lock_file


@pytest.fixture(scope="session")
def docker_client() -> docker.client:
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
def production_image(docker_client, hot_cookie: Result) -> str:
    setup_lock_file(hot_cookie)

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
def cleaned_up_test_container(docker_client, request) -> None:
    test_container_name: str = request.param
    yield test_container_name
    test_container = docker_client.containers.get(test_container_name)
    test_container.stop()
    test_container.remove()
