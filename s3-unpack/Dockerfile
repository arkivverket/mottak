ARG PYTHONIMAGE=python:3.9.4-slim

FROM $PYTHONIMAGE AS prepare
SHELL ["/bin/bash", "-o", "pipefail", "-c"]


RUN pip install --no-cache-dir poetry

WORKDIR /app
COPY poetry.lock /app
COPY pyproject.toml /app
RUN poetry config virtualenvs.in-project true \
	&& poetry install --no-dev --no-interaction


FROM $PYTHONIMAGE

ENV PATH=/app/.venv/bin:${PATH}
COPY --from=prepare /app/.venv /app/.venv
COPY --chmod=700 entrypoint.sh /
COPY app/ app/

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "app.s3-unpack"]
