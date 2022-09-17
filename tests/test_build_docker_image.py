from time import sleep
from uuid import uuid4

import pytest
from docker.models.containers import Container


@pytest.mark.parametrize(
    "cleaned_up_test_container", [str(uuid4())], indirect=True
)
def test_build_production_image(
    docker_client, production_image, cleaned_up_test_container
):
    test_container: Container = docker_client.containers.run(
        production_image,
        name=cleaned_up_test_container,
        ports={"80": "80"},
        detach=True,
    )
    sleep(3.0)
    assert test_container is not None
