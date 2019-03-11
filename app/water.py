from pyspark.sql import SparkSession
filename = "hdfs://namenode:8020/spark_ml/Weatherwater.csv"
sc = SparkSession \
    .builder \
    .master("spark://spark-master:7077") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.executor.memory", "1000m")\
    .appName("Weather prediction") \
    .getOrCreate()
# conf = SparkConf().setAppName("Weather prediction").setMaster("spark://spark-master:7077"").set("spark.cassandra.connection.host", "cassandra")
    #sc = SparkContext.getOrCreate(SparkConf())
# sc = SparkContext(conf = conf)
rawdata = sc.read.load(filename, format="csv", sep=",", inferSchema="true", header="true")
rawdata.printSchema()

rawdata.write.mode('overwrite').orc("hdfs://namenode:8020/spark_ml/Weather")

#Cassandra shit

#writing to cassandra
#  df.write\
#     .format("org.apache.spark.sql.cassandra")\
#     .mode('append')\
#     .options(table="tempgallons", keyspace="weatherwater")\
#     .save()
df = sc.read.format("org.apache.spark.sql.cassandra").option("table", "tempgallons").option("keyspace", "weatherwater" ).load()
print("After cassandra *********************************************************************")
df.show()
print("Finished cassandra *********************************************************************")
#sc.stop()
# df.select("name", "age").write.save("namesAndAges.parquet", format="parquet")