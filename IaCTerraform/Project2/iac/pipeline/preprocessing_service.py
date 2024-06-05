import os
import numpy as np
from proj_log import LoggerClass
from pyspark.ml.feature import *
from pyspark.sql import functions
from pyspark.sql.functions import *
from pyspark.ml.evaluation import *
from pyspark.ml.classification import *
from pyspark.sql.types import StringType, IntegerType
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

class SparkPreprocessor:

    def __init__(self) -> None:
        """
        Constructor for the class SparkPreprocessor to preprocess
        the data for the pipeline
        """
        # instantiate log
        self.log = LoggerClass()

    def calculate_missing_values(self, data: object) -> list:
        """
        Method to calculate the missing values in the dataset

        Parameters
        ----------
        data : object
            Dataframe with the data

        Returns
        -------
        list
            List with the missing values
        """
        null_cols_counts = []
        
        # number of rows
        num_rows = data.count()

        for k in data.columns:
            
            # count the nummber of missing rows
            nullRows = data.where(col(k).isNull()).count()

            if(nullRows > 0):
                # create a tuple with the name of the column and the number of missing rows
                # and the percentage of missing rows
                temp = k, nullRows, (nullRows/num_rows)*100

                # append the tuple to the list
                null_cols_counts.append(temp)

        return null_cols_counts
    
    def run(self, spark: object, bucket: object, bucket_name: str, env_EMR: bool) -> list:
        """
        Method to run the preprocessing pipeline

        Parameters
        ----------
        spark : object
            Spark session object
        bucket : object
            AWS Bucket object
        bucket_name : str
            name of the bucket
        env_EMR : bool
            flag to indicate if the environment is Amazon EMR

        Returns
        -------
        list
            list with the featurized datasets
        """
        # define the path to save the results
        path = f's3://{bucket_name}/data/' if env_EMR else 'data/'

        # log the reading
        self.log.log_msg('[INFO] Reading the dataset', bucket = bucket)

        # load the csv file
        safety_data = spark.read.csv(path + 'dataset.csv', header=True, escape='\"')

        # log the success
        self.log.log_msg('[INFO] Dataset read successfully', bucket = bucket)
        self.log.log_msg('[INFO] Total number of rows: ' + str(safety_data.count()), bucket = bucket)
        self.log.log_msg('[INFO] Checking for missing values', bucket = bucket)

        # calculate the missing values
        missing_values = self.calculate_missing_values(safety_data)

        # action based on the missing values
        if (len(missing_values) > 0):
            for col in missing_values:
                self.log.log_msg(f'[WARNINGS] Column: {col[0]} - Missing rows: {col[1]} - Percentage: {col[2]}%', bucket = bucket)
            
            # drop the rows with missing values
            safety_data = safety_data.dropna()
            self.log.log_msg('[INFO] Rows with missing values dropped', bucket = bucket)
            self.log.log_msg('[INFO] Total number of rows after dropping missing values: ' + str(safety_data.count()), bucket = bucket)
        else:
            self.log.log_msg('[INFO] No missing values found', bucket = bucket)

        # check class balancing
        self.log.log_msg('[INFO] Checking class balancing', bucket = bucket)
        count_low = safety_data.filter(safety_data['severities'] == 'low').count()
        count_medium = safety_data.filter(safety_data['severities'] == 'medium').count()
        count_high = safety_data.filter(safety_data['severities'] == 'high/critical').count()

        # log the class balancing
        self.log.log_msg(f'[INFO] Low Severity Reports: {count_low} - Medium Severity Reports: {count_medium} - High/Critical Severity Reports: {count_high}', bucket = bucket)

        # TODO - implement method for missing data
        # TODO - method for eliminating duplicated reports
        # TODO - method for eliminating reports starting with '('
        # TODO - method for indexing
        # TODO - method for tokenizing
        # TODO - method for removing stopwords
        # TODO - method for stemming
        # TODO - method for featurizing
        