FROM python:3.8-slim-buster
RUN apt-get update && apt-get install -y --no-install-recommends python3 git clamav-daemon clamav-freshclam && \
    apt-get clean && \
    freshclam && \
    pip install poetry && \
    mkdir -p /opt
WORKDIR /opt
COPY scanner.py _version.py start.sh pyproject.toml poetry.lock /opt/
COPY conf/clamd.conf /etc/clamav/clamd.conf
RUN poetry install
# If you wanna debug you might wanna drop your gcs.json into the container or perhaps bind-mount it or whatever.
# COPY gcs.json /opt
CMD ["/opt/start.sh"]
