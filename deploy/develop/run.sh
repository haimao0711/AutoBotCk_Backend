#!/bin/sh

# ==========================
# Config biến môi trường
# ==========================
CONTAINER_NAME="backend_vps"

# Dừng và xóa container cũ nếu có
OLD_CONTAINER=$(docker ps -a --quiet --filter "name=${CONTAINER_NAME}")
if [ -n "$OLD_CONTAINER" ]; then
  echo "♻️ Stopping and removing old container ${CONTAINER_NAME}..."
  docker stop $OLD_CONTAINER
  docker rm $OLD_CONTAINER
  echo "...[done] remove old container ${CONTAINER_NAME}"
fi

# Khởi chạy container mới với docker-compose
echo "🚀 Starting new container ${CONTAINER_NAME}..."
docker-compose -f docker-compose.yml up -d
echo "...[done] start new container ${CONTAINER_NAME}"
