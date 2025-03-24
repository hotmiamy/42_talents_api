#!/bin/bash

host="$1"
port="$2"
shift 2  # Remove host e port

# Processa os argumentos até encontrar --
while [ $# -gt 0 ]; do
    if [ "$1" = "--" ]; then
        shift
        break
    fi
    shift
done

cmd="$@"

export PGHOST="$host"
export PGPORT="$port"

max_retries=30
retry_count=0

until pg_isready -q || [ $retry_count -eq $max_retries ]; do
  echo "Waiting for PostgreSQL at $PGHOST:$PGPORT... ($((retry_count+1))/$max_retries)"
  retry_count=$((retry_count+1))
  sleep 2
done

if [ $retry_count -eq $max_retries ]; then
  echo "Failed to connect to PostgreSQL after $max_retries attempts"
  exit 1
fi

exec "$@"