#! /bin/sh

# Check container and re-run #
OLD_CONTAINER="$(docker ps --all --quiet --filter=name="backend_vps")"
if [ -n "$OLD_CONTAINER" ]; then
  docker stop $OLD_CONTAINER && docker rm $OLD_CONTAINER
  echo "...[done] remove old container backend_vps"
fi
docker stack deploy --compose-file docker-compose.yml --with-registry-auth stock-predict-api
echo "...[done] start new container backend_vps"


# #!/bin/sh

# set -e

# # Export biến tag để đồng bộ với build.sh
# export DOCKER_IMAGE_TAG="${CI_COMMIT_SHA:-latest}"

# # Remove old service (nếu có), không cần xóa container thủ công vì docker stack sẽ xử lý
# echo "...[info] deploying stack using image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

# # Re-deploy stack với registry auth để pull image private
# docker stack deploy \
#   --compose-file docker-compose.yml \
#   --with-registry-auth \
#   stock-predict-api

# echo "...[done] stack deployed using image ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
