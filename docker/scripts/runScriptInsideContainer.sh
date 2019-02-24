#!/bin/bash


export SCRIPT_PATH=./getData.sh
export CONTAINER_NAME=container_name
export DIST_PATH=/

echo "Copying the script in the container ${CONTAINER_NAME} in the folder ${DEST_PATH}"
docker cp ${SCRIPT_PATH} ${container_name}:${DEST_PATH}

echo "About to run the script ${SCRIPT_PATH} inside the container ${CONTAINER_NAME}"
docker exec -it ${CONTAINER_NAME} ./${DIST_PATH}