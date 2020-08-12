
FROM debian:buster-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget ca-certificates python3 python3-pip python3-psycopg2 \
    && apt-get clean

RUN wget -q https://github.com/tus/tusd/releases/download/v1.4.0/tusd_snapshot_amd64.deb && \
    dpkg -i tusd_snapshot_amd64.deb

RUN mkdir -p /srv/tusd-hooks /srv/tusd-data \
    && useradd --system --user-group tusd \
    && chown tusd:tusd /srv/tusd-data

# RUN pip3 install --upgrade pip
RUN pip3 install azure-servicebus
WORKDIR /srv/tusd-data
COPY tusd-hooks/pre-create  /srv/tusd-hooks/pre-create
COPY tusd-hooks/pre-create  /srv/tusd-hooks/post-finish
COPY start.sh /srv/start.sh

EXPOSE 1080
USER tusd

CMD ["/srv/start.sh"]
