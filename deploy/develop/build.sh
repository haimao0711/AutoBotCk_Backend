#!/bin/sh
# Load biến môi trường từ .env.production
export $(grep -v '^#' .env.production | xargs)

echo "Building Docker image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}..."

docker --version
docker buildx build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} . --push
docker images

echo "...[done] build image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
