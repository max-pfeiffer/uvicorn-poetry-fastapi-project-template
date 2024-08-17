"""Post gen hook for Cookiecutter."""

from pathlib import Path
from shutil import rmtree

REMOVE_PATHS: list[str] = [
    "{% if not cookiecutter.github_workflow %}.github{% endif %}",
]

for path in REMOVE_PATHS:
    if path and Path(path.strip()).exists():
        path_object: Path = Path(path.strip())
        path_object.unlink() if path_object.is_file() else rmtree(path_object)
