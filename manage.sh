#!/bin/bash

# Prosty skrót do zarządzania Django wewnątrz kontenera Docker

if [ "$#" -eq 0 ]; then
  echo "Użycie: ./manage.sh <komenda Django>"
  echo "Przykład: ./manage.sh migrate"
  exit 1
fi

docker-compose exec backend python manage.py "$@"
