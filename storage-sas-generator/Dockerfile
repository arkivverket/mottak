FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./pyproject.toml ./poetry.lock* /app/

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    cd /app/ && \
    poetry install --no-root --no-dev

ADD app /app/app

EXPOSE 80
