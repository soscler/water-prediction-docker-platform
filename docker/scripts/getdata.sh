#!/bin/bash

export DATA_FOLDER_NAME=spark_ml
export DATA_FILE_NAME=AdultCensusIncome.csv
export DATA_URL=https://amldockerdatasets.azureedge.net/AdultCensusIncome.csv

echo "Downloading the data set..."
if [ ! -f ${DATA_FOLDER_NAME}/${DATA_FILE_NAME} ]; then
	wget -O ${DATA_FOLDER_NAME}/${DATA_FILE_NAME}  ${DATA_FILE_URL};
fi
echo "Create the folder ${DATA_FOLDER_NAME} and put the data..."
hdfs dfs -mkdir ${DATA_FOLDER_NAME} &&  hdfs dfs -put ${DATA_FILE_NAME} ${DATA_FOLDER_NAME}/${DATA_FILE_NAME}