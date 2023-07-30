#!/bin/bash
while true
do
  echo "Running sync.py"
  python ./sync.py
  echo "Sleeping for ${INTERVAL} seconds"
  sleep "${INTERVAL}"
done