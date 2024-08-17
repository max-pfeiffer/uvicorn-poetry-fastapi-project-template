"""Tests for custom config."""

from pathlib import Path

import pytest
import toml
from dockerfile_parse import DockerfileParser
from pytest_cookies.plugin import Result


@pytest.mark.parametrize("python_version", ["3.12.0", "3.11.6", "3.10.13"])
@pytest.mark.parametrize("operating_system_variant", ["slim-bookworm", "bookworm"])
@pytest.mark.parametrize("github_workflow", [True, False])
def test_custom_config(
    cookies,
    python_version: str,
    operating_system_variant: str,
    github_workflow: bool,
) -> None:
    """
    Test for some random custom config.

    :param cookies: cookies fixture
    """
    result: Result = cookies.bake(
        extra_context={
            "project_name": "Seriously silly pRoject naMe",
            "project_version": "21.76.5",
            "project_description": "A project description which does make "
            "a lot of sense.",
            "author_name": "Jane Doe",
            "author_email": "jane.doe@unknown.com",
            "python_version": python_version,
            "operating_system_variant": operating_system_variant,
            "github_workflow": github_workflow,
        }
    )

    assert result.project_path.name == "seriously-silly-project-name"
    assert result.project_path.is_dir()

    # Check if pyproject.toml became expanded correctly
    pyproject_toml_file: Path = result.project_path / "pyproject.toml"
    toml_data: dict = toml.load(pyproject_toml_file)

    assert toml_data["tool"]["poetry"]["name"] == "Seriously silly pRoject naMe"
    assert toml_data["tool"]["poetry"]["version"] == "21.76.5"
    assert (
        toml_data["tool"]["poetry"]["description"]
        == "A project description which does make a lot of sense."
    )
    assert toml_data["tool"]["poetry"]["authors"] == ["Jane Doe <jane.doe@unknown.com>"]

    # Check if Dockerfile became expanded correctly
    dockerfile: Path = result.project_path / "Dockerfile"
    dfp = DockerfileParser(path=str(dockerfile))

    assert dfp.is_multistage
    assert all(
        [
            f"{python_version}-{operating_system_variant}" in image
            for image in dfp.parent_images
        ]
    )

    # Check for GitHub workflow
    workflow: Path = result.project_path / ".github" / "workflows" / "pipeline.yml"
    if github_workflow:
        assert workflow.exists()
    else:
        assert not workflow.exists()
