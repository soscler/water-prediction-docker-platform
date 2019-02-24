#!/bin/bash


export SUBMIT_IMAGE_NAME=submit-example 
export DOCKER_FILE_PATH=../submit/
export SCRIPTS_FOLDER=./
export APP_FOLDER=../../app


echo "Copying the dependency scripts..."
rm -rf ${DOCKER_FILE_PATH}/scripts/   ${DOCKER_FILE_PATH}/app/
mkdir ${DOCKER_FILE_PATH}/scripts/  ${DOCKER_FILE_PATH}/app/
cp -r ${SCRIPTS_FOLDER}/* ${DOCKER_FILE_PATH}/scripts
cp -r ${APP_FOLDER}/* ${DOCKER_FILE_PATH}/app


echo "About to build the image ${IMAGE_NAME}..." 
docker build ${DOCKER_FILE_PATH} -t ${SUBMIT_IMAGE_NAME}
echo "Removing unecessary files..."
rm -rf ${DOCKER_FILE_PATH}/scripts/
rm -rf ${DOCKER_FILE_PATH}/app