# Issues logs

#### Issue #01
#### Status: Resolved

Desc: connection between hdfs and spark

Steps to get the issue
#### before running these commands, you must be in the root folder of the project

-   Run the docker-compose file: It will launch all the containers for spark, hadoop, hue and spark notebook
```
docker-compose -f ./docker/compose/docker-compose.yml up -d
```
-   Inside the namenode container setup the data file and folder

```
docker cp ./resources/AdultCensusIncome.csv namenode:/
docker exec -ti namenode bash
hdfs dfs -mkdir /spark_ml
hdfs dfs -put AdultCensusIncome.csv /spark_ml/AdultCensusIncome.csv
```

-   Build the job submit image
```
./docker/scripts/buildSubmit.sh
```
-   Run the submit
```
docker run --rm --name submit --link spark-master:spark-master --network ml-spark-hdfs-docker_defaul submit 
or just run the script
./docker/scripts/submitJob
```
You must now see the errro:
*file:spark_ml/AdultCensusIncome.cvs does not exist*\
org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: file:/spark_ml/AdultCensusIncome.csv
