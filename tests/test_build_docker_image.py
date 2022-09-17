from time import sleep
from uuid import uuid4

import pytest
from docker.models.containers import Container
from furl import furl
from httpx import get, Response

from tests.constants import HELLO_WORLD, LOCALHOST, SLEEP_TIME, ITEMS


def call_api_endpoints():
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


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_production_image_build(
    docker_client, production_image, cleaned_up_test_container
):
    test_container: Container = docker_client.containers.run(
        production_image,
        name=cleaned_up_test_container,
        ports={"80": "80"},
        detach=True,
    )
    sleep(SLEEP_TIME)
    assert test_container is not None
    call_api_endpoints()


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_development_image_build(
    docker_client, development_image, cleaned_up_test_container
):
    test_container: Container = docker_client.containers.run(
        development_image,
        name=cleaned_up_test_container,
        ports={"80": "80"},
        detach=True,
    )
    sleep(SLEEP_TIME)
    assert test_container is not None
    call_api_endpoints()
