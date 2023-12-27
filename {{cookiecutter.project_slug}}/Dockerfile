# Using an image for dependency build stage which provides Poetry
# see: https://github.com/max-pfeiffer/python-poetry/blob/main/build/Dockerfile
FROM pfeiffermax/python-poetry:1.8.0-poetry1.7.1-python{{ cookiecutter.python_version }}-{{ cookiecutter.operating_system_variant }} as dependencies-build-stage
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR="/application_root/.cache" \
    PYTHONPATH=/application_root

# Set the WORKDIR to the application root.
# https://www.uvicorn.org/settings/#development
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR ${PYTHONPATH}

# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
COPY ./pyproject.toml ${PYTHONPATH}
RUN poetry install --no-interaction --no-root --without dev

# Using the standard Python image here to have the least possible image size
FROM python:{{ cookiecutter.python_version }}-{{ cookiecutter.operating_system_variant }} as production-image
ARG APPLICATION_SERVER_PORT=8000

    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED=1 \
    # https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/application_root \
    VIRTUAL_ENVIRONMENT_PATH="/application_root/.venv" \
    APPLICATION_SERVER_PORT=$APPLICATION_SERVER_PORT

# Adding the virtual environment to PATH in order to "activate" it.
# https://docs.python.org/3/library/venv.html#how-venvs-work
ENV PATH="$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# Principle of least privilege: create a new user for running the application
RUN groupadd -g 1001 python_application && \
    useradd -r -u 1001 -g python_application python_application

# Set the WORKDIR to the application root.
# https://www.uvicorn.org/settings/#development
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR ${PYTHONPATH}
RUN chown python_application:python_application ${PYTHONPATH}

# Copy virtual environment
COPY --from=dependencies-build-stage --chown=python_application:python_application ${VIRTUAL_ENVIRONMENT_PATH} ${VIRTUAL_ENVIRONMENT_PATH}

# Copy application files
COPY --chown=python_application:python_application /app ${PYTHONPATH}/app/

# Document the exposed port
# https://docs.docker.com/engine/reference/builder/#expose
EXPOSE ${APPLICATION_SERVER_PORT}

# Use the unpriveledged user to run the application
USER 1001

# Run the uvicorn application server.
CMD exec uvicorn --workers 1 --host 0.0.0.0 --port $APPLICATION_SERVER_PORT app.main:app
