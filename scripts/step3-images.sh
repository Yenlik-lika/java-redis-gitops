#!/usr/bin/env bash
# Қадам 3: v1 және v2 образдарын құрып, kind кластеріне жүктеу
set -e
for v in v1 v2; do
  docker build --build-arg APP_VERSION=$v -t java-app:$v app
  kind load docker-image java-app:$v --name devops
done
docker images | grep java-app
