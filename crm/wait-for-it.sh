#!/usr/bin/env bash
# wait-for-it.sh: script that waits for a service (e.g., a database) to be ready

host="$1"
shift
cmd="$@"

until nc -z "$host"; do
  >&2 echo "Waiting for $host"
  sleep 1
done

>&2 echo "$host is up - executing command"
exec $cmd
