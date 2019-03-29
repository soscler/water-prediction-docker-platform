#!/bin/bash

export JAR_FILE_FOLDER=../producer/
export JAR_FILE_NAME=kafka-producer-1.0-SNAPSHOT-jar-with-dependencies.jar
export DEST_PATH=/
export CONTAINER_NAME=spark-master

echo "About to copy ${JAR_FILE_NAME} to the container ${CONTAINER_NAME}..."
docker cp ${JAR_FILE_FOLDER}/${JAR_FILE_NAME} ${CONTAINER_NAME}:${DEST_PATH}
docker exec ${CONTAINER_NAME} java -jar ${JAR_FILE_NAME}
