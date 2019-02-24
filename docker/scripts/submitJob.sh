#!/bin/bash

export CONTAINER_NAME=submit
export LINK=spark-master:spark-master
export NETWORK= #ml-spark-hdfs-docker_defaul
export SUBMIT_IMAGE_NAME=#submit-example

echo "About to run the submit container..."
docker run --rm --name ${CONTAINER_NAME} --link ${LINK} --network ${NETWORK} ${SUBMIT_IMAGE_NAME}
