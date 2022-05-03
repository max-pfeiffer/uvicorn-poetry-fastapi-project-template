"""
Tests custom config
"""

from pathlib import Path

import toml
from pytest_cookies.plugin import Result


def test_custom_config(cookies) -> None:
    """
    Test for some random custom config.

    :param cookies: cookies fixture
    """
    # pylint: disable=duplicate-code
    result: Result = cookies.bake(
        extra_context={
            "project_name": "Seriously silly pRoject naMe",
            "project_version": "21.76.5",
            "project_description": "A project description which does make a lot of sense.",
            "author_name": "Jane Doe",
            "author_email": "jane.doe@unknown.com",
        }
    )

    assert result.project_path.name == "seriously-silly-project-name"
    assert result.project_path.is_dir()

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
