#!/bin/bash

export CONTAINER_NAME=submit
export LINK=spark-master:spark-master
export NETWORK=compose_default
export SUBMIT_IMAGE_NAME=submit

echo "About to run the submit container..."
docker run --rm --name ${CONTAINER_NAME} --link ${LINK} --network ${NETWORK}  ${SUBMIT_IMAGE_NAME}
