![pipeline workflow](https://github.com/max-pfeiffer/uvicorn-poetry-project-template/actions/workflows/pipeline.yml/badge.svg)
# uvicorn-poetry-project-template
[Cookiecutter](https://github.com/cookiecutter/cookiecutter) project template for the
[uvicorn-poetry Docker image](https://github.com/max-pfeiffer/uvicorn-poetry).

This Docker image provides a platform to run Python applications with [Uvicorn](https://github.com/encode/uvicorn) on [Kubernetes](https://kubernetes.io/) container orchestration system.
It provides [Poetry](https://python-poetry.org/) for managing dependencies and setting up a virtual environment in the container.

## Quick Start
[Install Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html) on your machine. Then:
```shell
cookiecutter https://github.com/max-pfeiffer/uvicorn-poetry-project-template
```
In project directory install dependencies:
```shell
poetry install
```
Run application in project directory:
```shell
poetry run uvicorn --workers 1 --host 0.0.0.0 --port 80 app.main:app
```
