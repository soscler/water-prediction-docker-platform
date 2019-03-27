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

    # brokers, topic = sys.argv[1:]
    # # Defining Kafka Consumer
    print('*************************************************************************************************************')
    kafkaStream = KafkaUtils.createStream(ssc=ssc, zkQuorum='localhost:9092', groupId='DemoConsumer',topics={'topic1':1})
    # kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    

    #lines = kafkaStream.map(lambda x: x[1])
    #lines.pprint()
    # counts = lines.flatMap(lambda line: line.split(" ")) \
    #     # .map(lambda word: (word, 1)) \
    #     # .reduceByKey(lambda a, b: a+b)
    # counts.pprint()

    # from pyspark.streaming.kafka import TopicAndPartition
    # topic = "test"
    # brokers = "localhost:9092"
    # partition = 0
    # start = 0
    # topicpartion = TopicAndPartition(topic, partition)
    # fromoffset = {topicpartion: int(start)}
    # kafkaDStream = KafkaUtils.createDirectStream(spark_streaming,[topic], \
    #         {"metadata.broker.list": brokers}, fromOffsets = fromoffset)

    ssc.start()
    ssc.awaitTermination()