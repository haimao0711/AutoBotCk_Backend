#!/bin/sh

# ==========================
# Config biến môi trường
# ==========================
DOCKER_IMAGE_NAME=backend_autobot
DOCKER_IMAGE_TAG=latest

echo "🔧 Building Docker image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ..."

# Kiểm tra Docker
docker --version

# Build image
docker buildx build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .

# Kiểm tra image
docker images

# (Tuỳ chọn) Push image lên registry nếu cần
# docker login -u <username> -p $(cat ~/.password.txt)
# docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}

echo "...[done] build image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
