#!/bin/bash

export SPARK_MASTER_URL=spark://${SPARK_MASTER_NAME}:${SPARK_MASTER_PORT}
export SPARK_HOME=/spark

wait-for-step.sh


execute-step.sh
if [ -f "${SPARK_APPLICATION_JAR_LOCATION}" ]; then
    echo "Submit application ${SPARK_APPLICATION_JAR_LOCATION} with main class ${SPARK_APPLICATION_MAIN_CLASS} to Spark master ${SPARK_MASTER_URL}"
    echo "Passing arguments ${SPARK_APPLICATION_ARGS}"
    /spark/bin/spark-submit \
        --class ${SPARK_APPLICATION_MAIN_CLASS} \
        --master ${SPARK_MASTER_URL} \
        ${SPARK_SUBMIT_ARGS} \
        ${SPARK_APPLICATION_JAR_LOCATION} ${SPARK_APPLICATION_ARGS}
else
    if [ -f "${SPARK_APPLICATION_PYTHON_LOCATION}" ]; then
        echo "Submit application ${SPARK_APPLICATION_PYTHON_LOCATION} to Spark master ${SPARK_MASTER_URL}"
        echo "Passing arguments ${SPARK_APPLICATION_ARGS}"
        PYSPARK_PYTHON=python3 /spark/bin/spark-submit \
            --master ${SPARK_MASTER_URL} \
            ${SPARK_SUBMIT_ARGS} \
            --conf spark.cassandra.connection.host=cassandra \
            --packages datastax:spark-cassandra-connector:2.4.0-s_2.11 \
            --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 \
            --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0 \
            --repositories https://dl.bintray.com/spark-packages/maven/ \
            ${SPARK_APPLICATION_PYTHON_LOCATION} ${SPARK_APPLICATION_ARGS}
    else
        echo "Not recognized application."
    fi
fi
finish-step.sh
