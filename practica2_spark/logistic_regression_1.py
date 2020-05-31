import numpy
from pyspark.ml.classification import LogisticRegression
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator


def castColumns(df):
	df = df.withColumn('_c0',df['_c0'].cast("float").alias('_c0'))
	df = df.withColumn('_c1',df['_c1'].cast("float").alias('_c1'))
	df = df.withColumn('_c2',df['_c2'].cast("int").alias('_c2'))
	df = df.withColumn('_c3',df['_c3'].cast("int").alias('_c3'))
	df = df.withColumn('_c4',df['_c4'].cast("int").alias('_c4'))
	df = df.withColumn('_c5',df['_c5'].cast("int").alias('_c5'))
	df = df.withColumn('_c6',df['_c6'].cast("int").alias('_c6'))
	
	return df

def deleteColumn(df):
	columns_to_drop = ['_c0', '_c1', '_c2', '_c3', '_c4', '_c5']
	
	df = df.drop(*columns_to_drop)
	
	return df

if __name__ == "__main__":

	# create Spark context with Spark configuration
	conf = SparkConf().setAppName("Practica 4")  

	sc = SparkContext(conf=conf)
	sql = SQLContext(sc)

	# Load training data
	df = sql.read.format("csv").load("./data_training.csv")	
	df = castColumns(df)
	
	#trainingData=df.rdd.map(lambda x:(Vectors.dense(x[0:-1]), int(x[-1]))).toDF(["features", "label"])
	ignore = ['_c6']
	assembler = VectorAssembler(
		inputCols=[x for x in df.columns if x not in ignore],
		outputCol='features')

	data = assembler.transform(df)
	data = data.withColumnRenamed("_c6", "label")
	data = deleteColumn(data)
	data.show()
	
	training, test = data.randomSplit([0.6, 0.4])

	lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
	# Fit the model
	lrModel = lr.fit(training)

	predict_train = lrModel.transform(training)
	predict_test = lrModel.transform(test)
	predict_test.select("label", "prediction").show(10)
	
	evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label")
	accuracy = evaluator.evaluate(predict_test)
	
	print("Test set accuracy = " + str(accuracy))
	print("Test Error = %g" % (1.0 - accuracy))
	sc.stop()