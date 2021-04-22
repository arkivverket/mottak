FROM python:3.9.4-slim AS prepare
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
	# Adds poetry bin to $PATH, so we don't need to link it to /usr/local/bin
	PATH=/opt/poetry/bin:${PATH}

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        curl \
        git \
    \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /app
COPY poetry.lock /app
COPY pyproject.toml /app
RUN poetry config virtualenvs.in-project true \
	&& poetry install --no-dev

FROM python:3.9.4-slim

ENV PATH=/app/.venv/bin:${PATH}

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        clamav-daemon \
        clamav-freshclam \
    \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && freshclam

COPY --chown=clamav --from=prepare /app/.venv /app/.venv
COPY --chown=clamav app/ /app/
COPY --chown=clamav conf/ /etc/clamav/

USER clamav
CMD ["python", "-m", "app.scanner"]
