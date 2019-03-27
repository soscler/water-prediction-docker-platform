#!/bin/bash

export DATA_FOLDER_NAME=/spark_ml
export DATA_FILE_NAME=AdultCensusIncome.csv
export DATA_URL=https://amldockerdatasets.azureedge.net/AdultCensusIncome.csv

mkdir -p ${DATA_FOLDER_NAME}
echo "Downloading the data set..."

if [ ! -f ${DATA_FOLDER_NAME}/${DATA_FILE_NAME} ]; then
	wget -O ${DATA_FOLDER_NAME}/${DATA_FILE_NAME}  ${DATA_URL};
fi
echo "Create the folder ${DATA_FOLDER_NAME} and put the data..."
pwd
hdfs dfs -mkdir -p ${DATA_FOLDER_NAME} &&  hdfs dfs -put -f ${DATA_FOLDER_NAME}/${DATA_FILE_NAME} ${DATA_FOLDER_NAME}/${DATA_FILE_NAME}