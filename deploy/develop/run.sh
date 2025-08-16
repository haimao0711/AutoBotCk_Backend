#!/bin/sh
# Load biến môi trường từ .env.production
export $(grep -v '^#' .env.production | xargs)

# Kiểm tra container cũ
OLD_CONTAINER=$(docker ps -a -q --filter "name=${DOCKER_CONTAINER_NAME}")
if [ -n "$OLD_CONTAINER" ]; then
  echo "Stopping and removing old container ${DOCKER_CONTAINER_NAME}..."
  docker stop $OLD_CONTAINER && docker rm $OLD_CONTAINER
  echo "...[done] removed old container ${DOCKER_CONTAINER_NAME}"
fi

# Deploy bằng Docker stack
echo "Deploying stack ${DOCKER_CONTAINER_NAME}..."
docker stack deploy --compose-file docker-compose.yml --with-registry-auth ${DOCKER_CONTAINER_NAME}
echo "...[done] stack ${DOCKER_CONTAINER_NAME} deployed"
