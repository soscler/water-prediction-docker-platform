from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext, Row
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SQLContext, Row
import json
from datetime import datetime
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

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

def write_streaming_to_cassandra(predictions):
    """"
    Using the cassandra connector package to write the predictions dataframe to the cassandra container
    """
    predictions.write.format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .option("table", "streaming").option("keyspace", "weatherwater" )\
        .save()
    return "***********************************************Cassandra Success*********************************************************"

def evaluate_model(spark,predictions):
    evaluator = RegressionEvaluator(labelCol="gallons", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)

    #creating data frame
    cSchema = StructType([StructField("date", StringType()),StructField("rmse", FloatType())])
    date_done = [str(datetime.strftime(datetime.now(),'%y/%m/%d/%H/%M'))]
    rmse_data = [rmse]
    rmse_df = spark.createDataFrame(list(zip(date_done,rmse_data)),schema=cSchema)

    rmse_df.write.format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .option("table", "rmse").option("keyspace", "weatherwater" )\
        .save()
    return rmse

def load_model(context):
     waterpredictor = context.read.load("hdfs://namenode:8020/spark_ml/Waterpredictor.mml")
     return waterpredictor

def consume_streaming(context,session):
    """"
    Consumes the data from the producer
    """
    
    ssc = StreamingContext(sparkContext=context, batchDuration=2)

    streams = KafkaUtils.createDirectStream(ssc, topics=['topic1'], kafkaParams={"metadata.broker.list": 'kafka:29092'},keyDecoder=lambda x: x, valueDecoder=lambda x: x)
    rows = streams.map(lambda x: json.loads(x[1]))
    def process(rdd):
        """
        Nested function that processes each RDD from the data stream
        """
        sqlc = SQLContext(context)
        df = sqlc.createDataFrame(rdd)
        processed_df = df.select(df["HH"].cast(IntegerType()).alias("HH"),\
                df["DD"].cast(FloatType()).alias("DD"),\
                df["P"].cast(FloatType()).alias("P"),\
                df["VV"].cast(FloatType()).alias("VV"),\
                df["FH"].cast(FloatType()).alias("FH"),\
                df["T"].cast(FloatType()).alias("T"),\
                df["U"].cast(FloatType()).alias("U"),\
                df["ID"].cast(IntegerType()).alias("HH"),\
                df["YYYYMMDD"].cast(TimestampType()).alias("YYYYMMDD"),\
                df["SQ"].cast(FloatType()).alias("SQ"))

        predictor = load_model(context)
        streaming_predicition = testing_prediction(processed_df,predictor)
        write_streaming_to_cassandra(streaming_predicition)
    
    rows.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()

def main():
    spark = SparkSession\
        .builder\
        .master("spark://spark-master:7077")\
        .config("spark.cassandra.connection.host", "cassandra")\
        .config("spark.executor.memory", "2000m")\
        .appName("Weather prediction")\
        .getOrCreate()
    
    #1   
    write_to_hdfs(sc)
    #2
    trainingSet, testingSet = data_process(sc)
    #3
    waterpredictor = model_regressor(trainingSet)
    #4
    predictions = testing_prediction(testingSet,waterpredictor)
    #5
    evaluate_model(sc,predictions)
    #6
    write_to_cassandra(predictions)
    
    # -- Kafka consumer

    print("*************************************************************************************************************")
    sc = spark.sparkContext
    consume_streaming(sc,spark)
    

if __name__ == "__main__":
    main()
    



