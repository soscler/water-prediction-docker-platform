from pyspark.sql import SparkSession
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import *

filename = "hdfs://namenode:8020/spark_ml/Weatherwater.csv"
sc = SparkSession \
    .builder \
    .master("spark://spark-master:7077") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.executor.memory", "2000m")\
    .appName("Weather prediction") \
    .getOrCreate()
rawdata = sc.read.load(filename, format="csv", sep=",", inferSchema="true", header="true")

rawdata.write.mode('overwrite').orc("hdfs://namenode:8020/spark_ml/Weather")



data = sc.read.orc("hdfs://namenode:8020/spark_ml/Weather")
#select features to be used
dataset = data.sort(asc('ID')).select("ID","YYYYMMDD","HH", "DD","FH","T","SQ","P","VV","U","Gallons")
count = dataset.count()
training = dataset.limit(int(count *0.9))
testing = dataset.subtract(training)

assembler = VectorAssembler(inputCols=["DD","FH","T","SQ","P","VV","U"], outputCol='features')
trainingData = assembler.transform(training)
#Linear regression model
# lr = GeneralizedLinearRegression(family="gaussian", link="identity", maxIter=10, regParam=0.3,labelCol="Gallons")
# lr = LinearRegression(maxIter =10, regParam=0.3, elasticNetParam =0.8, labelCol="Gallons")
dt = DecisionTreeRegressor(labelCol="Gallons")
model = dt.fit(trainingData)

print("After model *********************************************************************")

testingData = assembler.transform(testing)

predictions = model.transform(testingData).select("ID","YYYYMMDD", "HH","prediction")

predicitiondf = testing.select("ID","YYYYMMDD", "HH", "Gallons").join(predictions, testing.ID == predictions.ID, 'inner') \
                .drop(predictions.YYYYMMDD).drop(predictions.ID).drop(predictions.HH)\
                .withColumnRenamed("ID","id")\
                .withColumnRenamed("YYYYMMDD","yyyymmdd")\
                .withColumnRenamed("HH", "hh")\
                .withColumnRenamed("Gallons","gallons")\
                .sort(asc('ID'))


predicitiondf.write.format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .option("table", "testpredictions").option("keyspace", "weatherwater" )\
    .save()
    # .option("confirm.truncate", "true")\
    
print("After writing to cassandra *********************************************************************")

sc.stop()
