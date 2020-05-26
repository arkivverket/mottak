FROM mcr.microsoft.com/dotnet/core/runtime:3.1.1-buster-slim
RUN mkdir -p /opt
WORKDIR /opt
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip lsb-release curl gnupg2 python3-psycopg2
RUN wget https://github.com/arkivverket/arkade5/releases/download/v1.5.1/Arkade5CLI-1.5.1.zip
RUN unzip Arkade5CLI-1.5.1.zip
RUN chmod +x /opt/Arkade5CLI-1.5.1/arkade.sh

RUN wget https://github.com/kahing/goofys/releases/latest/download/goofys && \
    chmod +x goofys && \
    mv goofys /usr/local/bin/goofys


COPY get-mets.py /opt
COPY run.sh /opt
CMD ["/opt/run.sh"]
