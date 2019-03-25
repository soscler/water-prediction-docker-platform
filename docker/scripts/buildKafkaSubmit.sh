#!/bin/bash


export SUBMIT_IMAGE_NAME=kafkasubmit
export DOCKER_FILE_PATH=../kafkasubmit/
export SCRIPTS_FOLDER=./
export APP_FOLDER=../../app


echo "Copying the dependency scripts..."
rm -rf ${DOCKER_FILE_PATH}/scripts/   ${DOCKER_FILE_PATH}/src/
mkdir ${DOCKER_FILE_PATH}/scripts/  ${DOCKER_FILE_PATH}/src/
cp -rf ${SCRIPTS_FOLDER}/* ${DOCKER_FILE_PATH}/scripts
cp -rf ${APP_FOLDER}/* ${DOCKER_FILE_PATH}/src


echo "About to build the image ${IMAGE_NAME}..." 
docker build ${DOCKER_FILE_PATH} -t ${SUBMIT_IMAGE_NAME}
echo "Removing unecessary files..."
rm -rf ${DOCKER_FILE_PATH}/scripts/
rm -rf ${DOCKER_FILE_PATH}/src