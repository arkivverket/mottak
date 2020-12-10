FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends wget
RUN pip install poetry
RUN mkdir -p /app

# Downloading azcopy
RUN mkdir -p /app/azcopy
RUN wget -O azcopy.tar.gz https://aka.ms/downloadazcopy-v10-linux
RUN tar -C /app/azcopy/ --strip-components=1 -zxvf azcopy.tar.gz

COPY pyproject.toml poetry.lock /app/
COPY arkiv_downloader /app/arkiv_downloader

WORKDIR /app

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "arkiv_downloader/main.py"]
