FROM golang:1.15-buster AS builder

RUN mkdir -p /go/src/github.com/perbu/ && cd /go/src/github.com/perbu/ && git clone --depth 1 https://github.com/perbu/tusd.git
WORKDIR /go/src/github.com/perbu/tusd/
RUN go get -d -v ./...

RUN version="$(git tag -l --points-at HEAD)" && \
    commit=$(git log --format="%H" -n 1) && \
    GOOS=linux GOARCH=amd64 go build \
        -ldflags="-X github.com/tus/tusd/cmd/tusd/cli.VersionName=${version} -X github.com/tus/tusd/cmd/tusd/cli.GitCommit=${commit} -X 'github.com/tus/tusd/cmd/tusd/cli.BuildDate=$(date --utc)'" \
        -o "/go/bin/tusd" ./cmd/tusd/main.go && \
        rm -r /go/src/*


FROM python:3.8-slim

WORKDIR /srv/tusd-data

COPY --from=builder /go/bin/tusd /usr/local/bin/tusd

# Install poetry and required dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        libpq-dev \
		build-essential \
        curl \
	\
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/

RUN mkdir -p /srv/hooks /srv/tusd-data \
    && useradd --system --user-group tusd \
    && chown tusd:tusd /srv/tusd-data

COPY poetry.lock /srv
COPY pyproject.toml /srv
RUN poetry config virtualenvs.create false \
    && cd /srv \
    && poetry install --no-root --no-dev

COPY hooks  /srv/hooks
COPY start.sh /srv/start.sh

USER tusd
EXPOSE 1080
CMD ["/srv/start.sh"]
