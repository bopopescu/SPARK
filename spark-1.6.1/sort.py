from pyspark import SparkContext,SparkConf
import shutil,os

# non-spark code
if os.path.exists("../generated_file/result_py"):
    shutil.rmtree("../generated_file/result_py")

conf = SparkConf().setAppName("Sorting").setMaster("spark://n1.testspark.cs331-uc.emulab.net:7077").set("spark.eventLog.enabled","true").set("spark.eventLog.dir","../generated_driver_log/").set("spark.speculation","true")

sc = SparkContext(conf=conf)
text_file = sc.textFile("../generated_file/list_int",2)
counts = text_file.map(lambda a : (int(a),a)).sortByKey("true")

#print counts.collect()
counts.saveAsTextFile("../generated_file/result_py")

echo("daniar: done")

