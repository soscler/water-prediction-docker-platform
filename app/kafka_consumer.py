from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
   
    

    
if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("Usage: direct_kafka_wordcount.py <broker_list> <topic>", file=sys.stderr)
    #     sys.exit(-1)

    sc = SparkContext(appName="WeatherwaterKafkaConsumer", master="spark://spark-master:7077")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sparkContext=sc, batchDuration=1)

    streams = KafkaUtils.createDirectStream(ssc, topics=['topic1'], kafkaParams={"metadata.broker.list": 'kafka:29092'})
    lines = streams.map(lambda x: x[1])
    lines.pprint()
    #print(streams)

    ssc.start()
    ssc.awaitTermination()