from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
def kafkaConsumer():
    sc = SparkContext(appName="WeatherwaterKafkaConsumer")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, 2)
    
    # Defining Kafka Consumer
    kafkaStream = KafkaUtils.createDirectStream(ssc, 'cdh57-01-node-01.moffatt.me:2181', 'spark-streaming2', {'twitter':1})

    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
        sys.exit(-1)

    sc = SparkContext(appName="WeatherwaterKafkaConsumer")
    ssc = StreamingContext(sc, 2)

    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})


    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
