"""
Tests default config
"""

from pathlib import Path

import toml
from pytest_cookies.plugin import Result


def test_default_config(cookies) -> None:
    """
    Test for some random custom config.

    :param cookies: cookies fixture
    """
    # pylint: disable=duplicate-code
    result: Result = cookies.bake()

    assert result.project_path.name == "project-name"
    assert result.project_path.is_dir()

    pyproject_toml_file: Path = result.project_path / "pyproject.toml"
    toml_data: dict = toml.load(pyproject_toml_file)

    assert toml_data["tool"]["poetry"]["name"] == "Project Name"
    assert toml_data["tool"]["poetry"]["version"] == "0.0.0"
    assert toml_data["tool"]["poetry"]["description"] == ""
    assert toml_data["tool"]["poetry"]["authors"] == []
