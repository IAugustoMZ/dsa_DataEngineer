# if I want to install a package from the inside of the script
# import subprocess
# subprocess.run(["pip", "install", "boto3"])

# Main Scripts for Project 2
import os
import pyspark
import traceback
from aws_infra import AWSInfra
from proj_log import LoggerClass
from pyspark.sql import SparkSession

from spark_complete_pipeline_service import SafetyReportCompletePipeline

print('\n[INFO] Starting the Processing')

# instantiate log
log = LoggerClass()

# instantiate the AWSInfra class
aws_infra = AWSInfra()

# define the environment of execution of Amazon EMR
env_EMR = False if os.path.isdir('data/') else True

# create the bucket
bucket = aws_infra.get_bucket()
log.log_msg('[INFO] Found Bucket: ' + aws_infra.BUCKET_NAME, bucket = bucket)

# start Apache Spark 
log.log_msg('[INFO] Starting Apache Spark', bucket = bucket)

# create the Spark session
try:
    spark = SparkSession.builder.appName('SSTKSafetyMLClassifier').getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
except:
    log.log_msg('[ERROR] Error starting Apache Spark', bucket = bucket)
    log.log_msg(traceback.format_exc(), bucket = bucket)
    raise Exception(traceback.format_exc())

# in case of success, log the message
log.log_msg('[INFO] Apache Spark started successfully', bucket = bucket)

# instantiate the SafetyReportCompletePipeline class
report_pipeline = SafetyReportCompletePipeline(
    spark_session=spark,
    aws_bucket=bucket,
    bucket_name=aws_infra.BUCKET_NAME,
    environment_EMR=env_EMR
)

# run preprocessing pipeline
try:
    log.log_msg('[INFO] Running the preprocessing pipeline', bucket = bucket)
    DataHTFfeaturized, DataTFIDFfeaturized, DataW2Vfeaturized = report_pipeline.run_preprocessing()
except:
    log.log_msg('[ERROR] Error running the preprocessing pipeline', bucket = bucket)
    log.log_msg(traceback.format_exc(), bucket = bucket)
    spark.stop()
    raise Exception(traceback.format_exc())

# log the success of the preprocessing pipeline
log.log_msg('[INFO] Preprocessing pipeline ran successfully', bucket = bucket)

# run modeling pipeline
try:
    log.log_msg('[INFO] Running the modeling pipeline', bucket = bucket)
    report_pipeline.run_modeling([DataHTFfeaturized, DataTFIDFfeaturized, DataW2Vfeaturized])
except:
    log.log_msg('[ERROR] Error running the modeling pipeline', bucket = bucket)
    log.log_msg(traceback.format_exc(), bucket = bucket)
    spark.stop()
    raise Exception(traceback.format_exc())

# log the success of the modeling pipeline
log.log_msg('[INFO] Modeling pipeline ran successfully', bucket = bucket)

# log the saving of the models in S3
log.log_msg('[INFO] Models saved in S3 bucket', bucket = bucket)

# stop the Spark session
log.log_msg('[INFO] Stopping Apache Spark', bucket = bucket)
spark.stop()