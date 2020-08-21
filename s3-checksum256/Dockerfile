FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends python3 git
RUN mkdir -p /opt
RUN pip install poetry
# We don't need requirements.txt - we get native packages from debian.
# Install the helper module:
RUN useradd --home-dir /opt mol
WORKDIR /opt
COPY checksum.py _version.py pyproject.toml poetry.lock /opt/
RUN chown -R mol /opt
USER mol
RUN poetry install

# alpine seems to be a bit stupid wrt PYTHONPATH handling.
# COPY gcs.json /opt
# run the scanner - can be overriden when debugging.
CMD ["/usr/local/bin/poetry", "run", "/opt/checksum.py"]
