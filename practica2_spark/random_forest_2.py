import numpy
from pyspark.ml.classification import RandomForestClassifier
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler, IndexToString, StringIndexer, VectorIndexer
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

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
	
	ignore = ['_c6']
	assembler = VectorAssembler(
		inputCols=[x for x in df.columns if x not in ignore],
		outputCol='features')

	data = assembler.transform(df)
	data = data.withColumnRenamed("_c6", "label")
	data = deleteColumn(data)
	data.show()
	
	# Index labels, adding metadata to the label column.
	# Fit on whole dataset to include all labels in index.
	labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(data)
	
	# Automatically identify categorical features, and index them.
	# Set maxCategories so features with > 4 distinct values are treated as continuous.
	featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(data)
	
	# Split the data into training and test sets (30% held out for testing)
	(trainingData, testData) = data.randomSplit([0.7, 0.3])

	# Train a RandomForest model.
	rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=100)

	# Convert indexed labels back to original labels.
	labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=labelIndexer.labels)

	# Chain indexers and forest in a Pipeline
	pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])

	# Train model.  This also runs the indexers.
	model = pipeline.fit(trainingData)

	# Make predictions.
	predictions = model.transform(testData)

	# Select example rows to display.
	predictions.select("predictedLabel", "label", "features").show(5)

	# Select (prediction, true label) and compute test error
	evaluator = MulticlassClassificationEvaluator(
		labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
	accuracy = evaluator.evaluate(predictions)
	print("Test set accuracy = " + str(accuracy))
	print("Test Error = %g" % (1.0 - accuracy))

	rfModel = model.stages[2]
	print(rfModel)  # summary only
	
	sc.stop()