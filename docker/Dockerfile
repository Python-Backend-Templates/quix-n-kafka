# -----------------------------------------------------------
# Pre base image
# Installs base dependencies and sets up python
# -----------------------------------------------------------
FROM python:3.11 AS pre-base

ARG APP_DIR

WORKDIR /

RUN pip install pip==24.0 && \
    pip install poetry==1.8.3

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

RUN poetry config virtualenvs.in-project true && \
    poetry config virtualenvs.create true && \
    poetry config cache-dir /tmp/poetry_cache

COPY ./${APP_DIR}/poetry.lock ./${APP_DIR}/pyproject.toml ./


# -----------------------------------------------------------
# Pre base image with dependencies for DEVELOPMENT
# Installs python dependencies with poetry
# -----------------------------------------------------------
FROM pre-base AS pre-base-dev-dependencies

RUN poetry install --no-interaction && \
    # clear poetry cache
    rm -rf /tmp/poetry_cache


# Pre base image with dependencies for PRODUCTION
# Installs python dependencies with poetry
FROM pre-base AS pre-base-prod-dependencies

RUN poetry install --only main --no-interaction && \
    # clear poetry cache
    rm -rf /tmp/poetry_cache


# -----------------------------------------------------------
# Base image
# Copies python devendencies from pre base image for DEVELOPMENT and sets up python
# -----------------------------------------------------------
FROM python:3.11-slim AS dev-base

ARG APP_DIR

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir /apps/
WORKDIR /apps/

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

COPY --from=pre-base-dev-dependencies ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./${APP_DIR}/ ./


# -----------------------------------------------------------
# Base image
# Copies python devendencies from pre base image for PRODUCTION and sets up python
# -----------------------------------------------------------
FROM python:3.11-slim AS prod-base

ARG APP_DIR

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir /apps/
WORKDIR /apps/

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

COPY --from=pre-base-prod-dependencies ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./${APP_DIR}/ ./


# ***********************************************************
# Ready to use images from now on
# ***********************************************************


# -----------------------------------------------------------
# Producer for PRODUCTION
# -----------------------------------------------------------
FROM prod-base AS prod-producer

WORKDIR /apps/

COPY ./docker/producer/entrypoint.sh entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]

# -----------------------------------------------------------
# Producer for DEVELOPMENT
# -----------------------------------------------------------
FROM dev-base AS dev-producer

WORKDIR /apps/

COPY ./docker/producer/entrypoint.local.sh /entrypoint.sh

ENTRYPOINT ["bash", "/entrypoint.sh"]


# -----------------------------------------------------------
# Consumer for PRODUCTION
# -----------------------------------------------------------
FROM prod-base AS prod-consumer

WORKDIR /apps/

COPY ./docker/consumer/entrypoint.sh entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]

# -----------------------------------------------------------
# Consumer for DEVELOPMENT
# -----------------------------------------------------------
FROM dev-base AS dev-consumer

WORKDIR /apps/

COPY ./docker/consumer/entrypoint.local.sh /entrypoint.sh

ENTRYPOINT ["bash", "/entrypoint.sh"]

