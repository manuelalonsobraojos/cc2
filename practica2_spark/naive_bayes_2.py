import numpy
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline

# Metodo para la realizacion de casting de los datos de las columnas
def castColumns(df):
	df = df.withColumn('_c0',df['_c0'].cast("float").alias('_c0'))
	df = df.withColumn('_c1',df['_c1'].cast("float").alias('_c1'))
	df = df.withColumn('_c2',df['_c2'].cast("int").alias('_c2'))
	df = df.withColumn('_c3',df['_c3'].cast("int").alias('_c3'))
	df = df.withColumn('_c4',df['_c4'].cast("int").alias('_c4'))
	df = df.withColumn('_c5',df['_c5'].cast("int").alias('_c5'))
	df = df.withColumn('_c6',df['_c6'].cast("int").alias('_c6'))
	
	return df

# Metodo para la eliminacion de columnas sobrantes una vez agrupados los features
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
	df.show()
	
	# Se agrupan los features en vectores
	ignore = ['_c6']
	assembler = VectorAssembler(
		inputCols=[x for x in df.columns if x not in ignore],
		outputCol='features')
	
	data = assembler.transform(df)
	
	# Cambiamos el nombre de la columna label
	data = data.withColumnRenamed("_c6", "label")
	
	# Realizamos el escalado de los valores para eliminar valores negativos
	columns_to_scale = ['features']	
	scalers = [MinMaxScaler(inputCol='features', outputCol=col + "_scaled") for col in columns_to_scale]
	pipeline = Pipeline(stages=scalers)
	scalerModel = pipeline.fit(data)
	scaledData = scalerModel.transform(data)
	
	scaledData = deleteColumn(scaledData)
	# Eliminamos los features sin escalar y nos quedamos con los escalados
	scaledData = scaledData.drop('features')
	scaledData = scaledData.withColumnRenamed("features_scaled", "features")
	scaledData.show()
	
	# Division de los datos en entrenamiento y test
	splits = scaledData.randomSplit([0.7, 0.3], 1234)
	train = splits[0]
	test = splits[1]

	# create the trainer and set its parameters
	nb = NaiveBayes(smoothing=0.5, modelType="multinomial")

	# Entrenamiento del modelo
	model = nb.fit(train)

	# select example rows to display.
	predictions = model.transform(test)
	predictions.show()

	# compute accuracy on the test set
	evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
												  metricName="accuracy")
	accuracy = evaluator.evaluate(predictions)
	print("Test set accuracy = " + str(accuracy))
	
	sc.stop()