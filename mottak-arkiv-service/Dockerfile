FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    cd /app && \
    poetry install --no-root --no-dev

COPY ./app /app/app
