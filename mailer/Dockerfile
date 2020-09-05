FROM python:3.8-slim-buster

RUN pip install poetry && \
    mkdir -p /opt
COPY mailer.py poetry.lock pyproject.toml _version.py start.sh  /opt/
WORKDIR /opt
RUN poetry install --no-dev

CMD ["/opt/start.sh"]

