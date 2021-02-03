FROM mcr.microsoft.com/dotnet/runtime:5.0-buster-slim

RUN mkdir -p /opt
WORKDIR /opt/arkade5
RUN apt-get update && apt-get install -y --no-install-recommends unzip lsb-release gnupg2 fuse httpie wget
RUN http --ignore-stdin --json --output arkade5.zip --download POST "https://backend.arkade.arkivverket.no/api/arkade-downloads" \
 "arkadeUI=CLI" "downloaderA1Xp=1" "downloaderEmail=perbue@arkivverket.no"  "downloaderNews=0" "orgAddress=0" "orgForm=0" "orgName=0" "orgNumber=0"
RUN unzip arkade5.zip && rm arkade5.zip && chmod +x /opt/arkade5/arkade.sh

RUN wget https://github.com/kahing/goofys/releases/latest/download/goofys && \
    chmod +x goofys && \
    mv goofys /usr/local/bin/goofys

COPY run.sh /opt
CMD ["/opt/run.sh"]
