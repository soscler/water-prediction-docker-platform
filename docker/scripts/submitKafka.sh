#!/bin/bash

export CONTAINER_NAME=kafkasubmit
export LINK=spark-master:spark-master
export NETWORK=scac-network-2019
export SUBMIT_IMAGE_NAME=kafkasubmit

echo "About to run the submit container..."
docker run --rm --name ${CONTAINER_NAME} --link ${LINK} --network ${NETWORK}  ${SUBMIT_IMAGE_NAME}
