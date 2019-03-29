from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def write_to_hdfs(spark): 
    filename = "hdfs://namenode:8020/spark_ml/Weatherwater2.csv"
    rawdata = spark.read.load(filename, format="csv", sep=",", inferSchema="true", header="true")
    rawdata.write.mode('overwrite').orc("hdfs://namenode:8020/spark_ml/Weather")

def feature_assembler():
    # creating a features column that is a array of all the learning features
    assembler = VectorAssembler(inputCols=["DD","FH","T","SQ","P","VV","U"], outputCol='features')
    return assembler

def data_process(spark):
    """
    data_process splits up the original dataset with preprocessing and selection of features to be used
    """
    #read from hdfs
    data = spark.read.orc("hdfs://namenode:8020/spark_ml/Weather")
    #select features to be used and also drop rows with missing values
    dataset = data\
        .sort(asc('ID'))\
        .select("ID","YYYYMMDD","HH", "DD","FH","T","SQ","P","VV","U","Gallons")\
        .na.drop() 

    #splitting the data into training and testing sets
    count = dataset.count()
    training = dataset.limit(int(count *0.9))
    testing = dataset.subtract(training)

    return training,testing
    

def model_regressor(trainingSet):
    """
    Model regressor using the spark ML decisionTree regressor. The algorithm expects a features column which
    is an array of the features being learnt and a label colum of the target value. 
    """
    trainingData = feature_assembler().transform(trainingSet)
    dt = DecisionTreeRegressor(labelCol="Gallons")
    model = dt.fit(trainingData)
    # saving the model 
    model_name = "Waterpredictor.mml"
    model_fs = "hdfs://namenode:8020/spark_ml/" + model_name

    model.write().overwrite().save(model_fs)
    print("saved model to {}".format(model_fs))
    return model


def testing_prediction(testSet, model):
    #transforming the testset
    testingData = feature_assembler().transform(testSet)
    predictions = model.transform(testingData).select("ID","YYYYMMDD", "HH","prediction")

    predicition_df = testSet.select("ID","YYYYMMDD", "HH", "Gallons","T").join(predictions, testSet.ID == predictions.ID, 'inner') \
                    .drop(predictions.YYYYMMDD).drop(predictions.ID).drop(predictions.HH)\
                    .withColumnRenamed("ID","id")\
                    .withColumnRenamed("YYYYMMDD","yyyymmdd")\
                    .withColumnRenamed("HH", "hh")\
                    .withColumnRenamed("T", "temperature")\
                    .withColumnRenamed("Gallons","gallons")\
                    .sort(asc('ID'))
    return predicition_df

def write_to_cassandra(predictions):
    """"
    Using the cassandra connector package to write the predictions dataframe to the cassandra container
    """
    predictions.write.format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .option("table", "testpredictions").option("keyspace", "weatherwater" )\
        .save()
    return "Cassandra Success"

def evaluate_model(predicitons):
    evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)

    #creating data frame
    cSchema = StructType([StructField("date", StringType()),StructField("rmse", FloatType())])
    rmse_list = [str(datetime.strftime(datetime.now(),'%y/%m/%d/%H/%M')), rmse]
    rmse_df = spark.createDataFrame(rmse_list,schema=cSchema )

    rmse_df.write.format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .option("table", "rmse").option("keyspace", "weatherwater" )\
        .save()
    return rmse

def main():
    # config = SparkConf()\
    #     .setMaster("spark://spark-master:7077") \
    #     .set("spark.cassandra.connection.host", "cassandra") \
    #     .set("spark.executor.memory", "2000m")
    # sc = SparkContext(appName="WeatherwaterKafkaConsumer", master="spark://spark-master:7077", conf=config) \
    #     .getOrCreate()
    sc = SparkSession \
        .builder \
        .master("spark://spark-master:7077") \
        .config("spark.cassandra.connection.host", "cassandra") \
        .config("spark.executor.memory", "2000m")\
        .appName("Weather prediction") \
        .getOrCreate()
    #1   
    #write_to_hdfs(sc)
    #2
    #trainingSet, testingSet = data_process(sc)
    #3
    #waterpredictor = model_regressor(trainingSet)
    
    # waterpredictor = sc.read.load("hdfs://namenode:8020/spark_ml/Waterpredictor.mml")
    #4
    #predictions = testing_prediction(testingSet,waterpredictor)
    #5
    #write_to_cassandra(predictions)
    #6

    # -- Kafka consumer

    print("*************************************************************************************************************")
    kafkareader = sc \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "topic1") \
        .option("startingOffsets", "earliest") \
        .load()
    # stream = kafkareader.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    # stream.writeStream.format("console").start()


    rawQuery = kafkareader \
        .writeStream \
        .queryName("qraw")\
        .format("memory")\
        .start()
    raw = sc.sql("select * from qraw")
    raw.show()

    # ssc = StreamingContext(sparkContext=sc, batchDuration=1)

    # streams = KafkaUtils.createDirectStream(ssc, topics=['topic1'], kafkaParams={"metadata.broker.list": 'kafka:29092'})
    # lines = streams.map(lambda x: x[1])
    # lines.pprint()
    # #print(streams)

    # ssc.start()
    # ssc.awaitTermination()
    sc.stop()

if __name__ == "__main__":
    main()
    



