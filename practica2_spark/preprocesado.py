import sys
 
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.ml.classification import LogisticRegression

def getHeaders(sql):
	df = sql.read.format("csv").option("delimiter"," ").load("/user/datasets/ecbdl14/ECBDL14_IR2.header")
	list = df.select('_c1').collect()
	mvv_array = [str(row._c1) for row in list]
	mvv_array.pop(0)
	mvv_array.pop(634)
	mvv_array.pop(633)
	mvv_array.pop(632)
	
	return mvv_array

if __name__ == "__main__":
 
	# create Spark context with Spark configuration
	conf = SparkConf().setAppName("Practica 4")  

	sc = SparkContext(conf=conf)
	sql = SQLContext(sc)

	df = sql.read.format("csv").options(delimiter=",", header='false').load("/user/datasets/ecbdl14/ECBDL14_IR2.data")
	header_list = getHeaders(sql)
	oldSchema = df.schema
	for i,k in enumerate(oldSchema.fields):
		k.name = header_list[i]
	
	df = sql.read.format("csv").options(delimiter=",", header='false').load("/user/datasets/ecbdl14/ECBDL14_IR2.data", schema=oldSchema)
	df.show()

	aux = df.select([c for c in df.columns if c in ['PSSM_r1_-1_D','PSSM_r1_4_N','AA_freq_global_Y', 'PSSM_central_-1_V', 'PredSA_freq_global_0', 'PSSM_r1_4_A', 'class']])
	aux.show()
	aux.write.format("csv").save("/user/ccsa74746291/filteredCH.small.training", header = 'true')
	sc.stop()