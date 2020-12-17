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

FROM debian:buster-slim

COPY --from=builder /go/bin/tusd /usr/local/bin/tusd

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget ca-certificates python3 python3-pip python3-psycopg2 \
    && apt-get clean

RUN mkdir -p /srv/hooks /srv/tusd-data \
    && useradd --system --user-group tusd \
    && chown tusd:tusd /srv/tusd-data




# RUN pip3 install --upgrade pip
RUN pip3 install azure-servicebus==0.50.3
WORKDIR /srv/tusd-data
COPY hooks  /srv/hooks
COPY start.sh /srv/start.sh
EXPOSE 1080
USER tusd

CMD ["/srv/start.sh"]
