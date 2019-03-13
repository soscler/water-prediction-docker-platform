#!/bin/bash

export FILE_NAME=getWaterData.sh
export SCRIPT_PATH=./${FILE_NAME}
export CONTAINER_NAME=namenode
export DEST_PATH=/spark_ml

echo "Copying the script ${FILE_NAME} in the container ${CONTAINER_NAME} in the folder ${DEST_PATH}"
docker exec ${CONTAINER_NAME} mkdir -p ${DEST_PATH}
docker cp ${SCRIPT_PATH} ${CONTAINER_NAME}:${DEST_PATH}

echo "About to run the script ${SCRIPT_PATH} inside the container ${CONTAINER_NAME}"
docker exec -it ${CONTAINER_NAME} ./${DEST_PATH}/${FILE_NAME}