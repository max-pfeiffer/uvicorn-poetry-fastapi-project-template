[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/max-pfeiffer/uvicorn-poetry-project-template/branch/main/graph/badge.svg?token=WQI2SJJLZN)](https://codecov.io/gh/max-pfeiffer/uvicorn-poetry-project-template)
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
Build the production Docker image:
```shell
docker build --tag my-application:1.0.0 .
```
Run the containerized application:
```shell
docker run -it --rm my-application:1.0.0
```
