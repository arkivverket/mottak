#!/bin/sh
set -e
echo "Refreshing ClamAV signatures"
freshclam --quiet
echo "Starting ClamAV"
clamd &
echo "Waiting for ClamAV to start"
wait-for-it localhost:3310 --strict --timeout=30 -- python /app/scanner.py
