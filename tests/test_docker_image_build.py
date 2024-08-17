"""Tests for Docker image build."""

from time import sleep
from uuid import uuid4

import pytest
from docker.client import DockerClient
from docker.models.containers import Container
from furl import furl
from httpx import Response, get

from tests.constants import HELLO_WORLD, ITEMS, LOCALHOST, SLEEP_TIME


def call_api_endpoints():
    """Call API endpoints.

    :return:
    """
    furl_item = furl(LOCALHOST)
    url = furl_item.url

    response: Response = get(url)
    assert response.status_code == 200
    assert HELLO_WORLD == response.json()

    for key, value in ITEMS.items():
        furl_item = furl(LOCALHOST)
        furl_item.path /= "items"
        furl_item.path /= key
        url = furl_item.url

        response: response = get(url)
        assert value == response.json()


@pytest.mark.parametrize("cleaned_up_test_container", [str(uuid4())], indirect=True)
def test_production_image_build(
    docker_client: DockerClient,
    production_image: str,
    cleaned_up_test_container,
):
    """Test production image.

    :param docker_client:
    :param production_image:
    :param cleaned_up_test_container:
    :return:
    """
    test_container: Container = docker_client.containers.run(
        production_image,
        name=cleaned_up_test_container,
        ports={"8000": "80"},
        detach=True,
    )
    sleep(SLEEP_TIME)
    assert test_container is not None
    call_api_endpoints()
