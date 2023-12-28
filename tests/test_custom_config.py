from pathlib import Path

import toml
from pytest_cookies.plugin import Result
from dockerfile_parse import DockerfileParser


def test_custom_config(cookies) -> None:
    """
    Test for some random custom config.

    :param cookies: cookies fixture
    """
    result: Result = cookies.bake(
        extra_context={
            "project_name": "Seriously silly pRoject naMe",
            "project_version": "21.76.5",
            "project_description": "A project description which does make a lot of sense.",
            "author_name": "Jane Doe",
            "author_email": "jane.doe@unknown.com",
            "python_version": "3.10.13",
            "operating_system_variant": "bookworm",
            "github_workflow": False,
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
    assert toml_data["tool"]["poetry"]["authors"] == [
        "Jane Doe <jane.doe@unknown.com>"
    ]

    # Check if Dockerfile became expanded correctly
    dockerfile: Path = result.project_path / "Dockerfile"
    dfp = DockerfileParser(path=str(dockerfile))

    assert dfp.is_multistage
    assert all(["3.10.13-bookworm" in image for image in dfp.parent_images])

    # Check for GitHub workflow
    workflow: Path = (
        result.project_path / ".github" / "workflows" / "pipeline.yml"
    )
    assert not workflow.exists()
