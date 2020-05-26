FROM python:3.8-slim-buster
RUN apt-get update && apt-get install -y --no-install-recommends python3 git && apt-get clean
RUN pip install poetry
RUN mkdir -p /opt
WORKDIR /opt
COPY s3-unpack.py start.sh pyproject.toml poetry.lock /opt/
RUN poetry install
# If you wanna debug you might wanna drop your gcs.json into the container or perhaps bind-mount it or whatever.
# COPY gcs.json /opt
CMD ["/opt/start.sh"]