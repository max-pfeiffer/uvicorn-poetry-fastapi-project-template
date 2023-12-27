from pathlib import Path

import toml
from pytest_cookies.plugin import Result
from dockerfile_parse import DockerfileParser


def test_default_config(cookies) -> None:
    """
    Test for some random custom config.

    :param cookies: cookies fixture
    """
    result: Result = cookies.bake()

    assert result.project_path.name == "project-name"
    assert result.project_path.is_dir()

    # Check if pyproject.toml became expanded correctly
    pyproject_toml_file: Path = result.project_path / "pyproject.toml"
    toml_data: dict = toml.load(pyproject_toml_file)

    assert toml_data["tool"]["poetry"]["name"] == "Project Name"
    assert toml_data["tool"]["poetry"]["version"] == "0.0.0"
    assert toml_data["tool"]["poetry"]["description"] == ""
    assert toml_data["tool"]["poetry"]["authors"] == []

    # Check if Dockerfile became expanded correctly
    dockerfile: Path = result.project_path / "Dockerfile"
    dfp = DockerfileParser(path=str(dockerfile))

    assert dfp.is_multistage
    assert all(["3.12.0-slim-bookworm" in image for image in dfp.parent_images])
