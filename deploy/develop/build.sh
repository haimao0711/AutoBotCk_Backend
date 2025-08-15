#! /bin/sh
printenv > .env
# Build docker image #
docker --version
docker buildx build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} . --push
docker images
echo "...[done] build image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"


# #!/bin/sh

# set -e

# # Ghi lại biến môi trường để container có thể sử dụng
# printenv > .env

# # In thông tin docker
# docker --version

# # Sử dụng CI_COMMIT_SHA làm tag nếu có, để đảm bảo uniqueness
# export DOCKER_IMAGE_TAG="${CI_COMMIT_SHA:-latest}"

# # Build image và push lên registry
# docker buildx build \
#   --no-cache \
#   --push \
#   -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} \
#   -f Dockerfile .

# docker images | grep ${DOCKER_IMAGE_NAME}
# echo "...[done] build image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
