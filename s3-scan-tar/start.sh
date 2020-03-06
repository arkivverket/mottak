#!/bin/sh
set -e
echo Refreshing ClamAV signatures
freshclam
echo Starting ClamAV
service clamav-daemon start
echo Initializing scan...
poetry run /opt/s3-scan-tar.py
