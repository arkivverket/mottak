FROM python:3.8-slim AS prepare
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
	#
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

FROM python:3.8-slim
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /app
ENV PATH=/app/.venv/bin:${PATH}
COPY --from=prepare /app/.venv /app/.venv

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        clamav-daemon \
        clamav-freshclam \
    \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && freshclam

COPY conf/clamd.conf /etc/clamav/clamd.conf

# permission juggling because we don't use clamd as a service
RUN mkdir /var/run/clamav \
    && chown clamav:clamav /var/run/clamav \
    && chmod 750 /var/run/clamav
COPY scanner.py /app/


# If you wanna debug you might wanna drop your gcs.json into the container or perhaps bind-mount it or whatever.
# COPY gcs.json /opt
CMD ["/app/scanner.py"]
