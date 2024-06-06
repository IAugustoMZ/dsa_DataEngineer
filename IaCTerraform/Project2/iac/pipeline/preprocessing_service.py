import os
import numpy as np
from aws_infra import AWSInfra
from proj_log import LoggerClass
from pyspark.ml.feature import *
from pyspark.sql import functions
from pyspark.sql.functions import *
from pyspark.ml.evaluation import *
from pyspark.ml.classification import *
from pyspark.sql.types import StringType, IntegerType
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

class SparkPreprocessor:

    # definition of the vectorizer
    vectorizers = {
        'htf': HashingTF(inputCol='filtered_tokens', outputCol='rawfeatures'),
        'tfidf': IDF(inputCol='rawfeatures', outputCol='features'),
        'w2v': Word2Vec(vectorSize=250, minCount=5, inputCol='filtered_tokens', outputCol='features')
    }

    def __init__(self) -> None:
        """
        Constructor for the class SparkPreprocessor to preprocess
        the data for the pipeline
        """
        # instantiate log
        self.log = LoggerClass()

        # instantiate the AWSInfra class
        self.aws_infra = AWSInfra()

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
    
    def check_and_treat_missing_values(self, data: object, bucket: object) -> object:
        """
        Method to check and treat missing values in the dataset

        Parameters
        ----------
        data : object
            Dataframe with the data
        bucket : object
            AWS Bucket object to log the messages

        Returns
        -------
        object
            Dataframe with the missing values treated
        """
        # calculate the missing values
        missing_values = self.calculate_missing_values(data)

        # action based on the missing values
        if (len(missing_values) > 0):
            for col in missing_values:
                self.log.log_msg(f'[WARNING] Column: {col[0]} - Missing rows: {col[1]} - Percentage: {col[2]}%', bucket = bucket)
            
            # drop the rows with missing values
            data = data.dropna()
            self.log.log_msg('[INFO] Rows with missing values dropped', bucket = bucket)
            self.log.log_msg('[INFO] Total number of rows after dropping missing values: ' + str(data.count()), bucket = bucket)
        else:
            self.log.log_msg('[INFO] No missing values found', bucket = bucket)

        return data
    
    def eliminate_duplicates(self, data: object, bucket: object) -> object:
        """
        Method to eliminate duplicated rows in the dataset

        Parameters
        ----------
        data : object
            Dataframe with the data
        bucket : object
            AWS Bucket object to log the messages

        Returns
        -------
        object
            Dataframe with duplicated rows eliminated
        """
        # check for duplicates
        num_rows = data.count()
        num_rows_no_duplicates = data.dropDuplicates(['reports']).count()

        # log the number of duplicates
        self.log.log_msg(f'[INFO] Number of duplicated reports: {num_rows - num_rows_no_duplicates}', bucket = bucket)

        # drop duplicates
        data = data.dropDuplicates(['reports'])

        return data
    
    def remove_rows_starting_with_symbol(self, data: object, bucket: object) -> object:
        """
        Method to remove rows that start with '(' in the 'reports' column

        Parameters
        ----------
        data : object
            Dataframe with the data
        bucket : object
            AWS Bucket object to log the messages

        Returns
        -------
        object
            Dataframe with rows removed
        """
        # count the number of rows starting with '('
        num_rows_starting_with_symbol = data.filter(data['reports'].startswith('(')).count()

        # log the count
        self.log.log_msg(f'[INFO] Number of rows starting with \'(\': {num_rows_starting_with_symbol}', bucket = bucket)

        # remove the rows starting with '('
        data = data.filter(~data['reports'].startswith('('))

        return data
    
    def string_indexer(self, data: object) -> object:
        """
        Method to fit a StringIndexer in the 'severities' column and transform the data

        Parameters
        ----------
        data : object
            Dataframe with the data

        Returns
        -------
        object
            Dataframe with the 'severities' column transformed
        """
        # create a StringIndexer object
        indexer = StringIndexer(inputCol='severities', outputCol='class')

        # fit the StringIndexer on the data
        indexer_model = indexer.fit(data)

        # transform the data
        transformed_data = indexer_model.transform(data)

        return transformed_data
    
    def remove_special_characters(self, data: object) -> object:
        """
        Method to remove special characters from the 'reports' column using regular expressions

        Parameters
        ----------
        data : object
            Dataframe with the data

        Returns
        -------
        object
            Dataframe with special characters removed
        """
        # remove special characters from the 'reports' column
        data = data.withColumn("reports", regexp_replace(data["reports"], '<.*/>', ''))
        data = data.withColumn("reports", regexp_replace(data["reports"], '[^A-Za-z ]+', ''))
        data = data.withColumn("reports", regexp_replace(data["reports"], ' +', ' '))

        # make every character lowercase
        data = data.withColumn("reports", lower(data["reports"]))

        return data
    
    def tokenize_reports(self, data: object) -> object:
        """
        Method to tokenize the 'reports' column

        Parameters
        ----------
        data : object
            Dataframe with the data

        Returns
        -------
        object
            Dataframe with the 'reports' column tokenized
        """
        # create a Tokenizer object
        tokenizer = RegexTokenizer(inputCol='reports', outputCol='tokens', pattern='\\W')

        # tokenize the 'reports' column
        tokenized_data = tokenizer.transform(data)

        return tokenized_data
    
    def remove_stopwords(self, data: object) -> object:
        """
        Method to remove stop words from the 'tokens' column

        Parameters
        ----------
        data : object
            Dataframe with the data

        Returns
        -------
        object
            Dataframe with stop words removed
        """
        # create a StopWordsRemover object
        remover = StopWordsRemover(inputCol='tokens', outputCol='filtered_tokens')

        # remove stop words from the 'tokens' column
        filtered_data = remover.transform(data)

        return filtered_data
    
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

        # check and treat missing values
        try:
            safety_data = self.check_and_treat_missing_values(safety_data, bucket)
        except:
            self.log.log_msg('[ERROR] Error checking and treating missing values', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # check class balancing
        self.log.log_msg('[INFO] Checking class balancing', bucket = bucket)
        count_low = safety_data.filter(safety_data['severities'] == 'low').count()
        count_medium = safety_data.filter(safety_data['severities'] == 'medium').count()
        count_high = safety_data.filter(safety_data['severities'] == 'high/critical').count()

        # log the class balancing
        self.log.log_msg(f'[INFO] Low Severity Reports: {count_low} - Medium Severity Reports: {count_medium} - High/Critical Severity Reports: {count_high}', bucket = bucket)

        # eliminate duplicates
        self.log.log_msg('[INFO] Eliminating duplicates', bucket = bucket)
        try:
            safety_data = self.eliminate_duplicates(safety_data, bucket)
        except:
            self.log.log_msg('[ERROR] Error eliminating duplicates', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # remove rows starting with '('
        self.log.log_msg('[INFO] Removing rows starting with \'(\'', bucket = bucket)
        try:
            safety_data = self.remove_rows_starting_with_symbol(safety_data, bucket)
        except:
            self.log.log_msg('[ERROR] Error removing rows starting with \'(\'', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # string indexer
        self.log.log_msg('[INFO] Transforming the data - applying indexing', bucket = bucket)
        try:
            safety_data = self.string_indexer(safety_data)
        except:
            self.log.log_msg('[ERROR] Error applying indexing', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # remove special characters
        self.log.log_msg('[INFO] Transforming the data - removing special characters', bucket = bucket)
        try:
            safety_data = self.remove_special_characters(safety_data)
        except:
            self.log.log_msg('[ERROR] Error removing special characters', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # tokenize reports
        self.log.log_msg('[INFO] Transforming the data - tokenizing reports', bucket = bucket)
        try:
            safety_data = self.tokenize_reports(safety_data)
        except:
            self.log.log_msg('[ERROR] Error tokenizing reports', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # remove stop words
        self.log.log_msg('[INFO] Transforming the data - removing stop words', bucket = bucket)
        try:
            safety_data = self.remove_stopwords(safety_data)
        except:
            self.log.log_msg('[ERROR] Error removing stop words', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())
        
        # apply the vectorizers
        featurized_data = {}
        for key, vectorizer in self.vectorizers.items():
            self.log.log_msg(f'[INFO] Applying {key}', bucket = bucket)
            try:
                featurized_data[key] = vectorizer.fit(safety_data).transform(safety_data)
            except:
                self.log.log_msg(f'[ERROR] Error applying {key}', bucket = bucket)
                self.log.log_msg(traceback.format_exc(), bucket = bucket)
                spark.stop()
                raise Exception(traceback.format_exc())
            
        # recover the data
        HTFfeaturizedData = featurized_data['htf']
        TFIDFfeaturizedData = featurized_data['tfidf']
        W2VfeaturizedData = featurized_data['w2v']

        # change the name of the objects
        HTFfeaturizedData.name = 'HTFfeaturizedData'
        HTFfeaturizedData = HTFfeaturizedData.withColumnRenamed('rawfeatures', 'features')
        TFIDFfeaturizedData.name = 'TFIDFfeaturizedData'
        W2VfeaturizedData.name = 'W2VfeaturizedData'

        # selecting the right columns from W2VfeaturizedData
        W2VfeaturizedData = W2VfeaturizedData.select('reports', 'class', 'features')

        # saving the data back to S3
        self.log.log_msg('[INFO] Saving the cleaned and transformed data', bucket = bucket)
        s3_path = 'data/'
        try:
            self.aws_infra.upload_processed_data(HTFfeaturizedData, path + 'HTFfeaturizedData', s3_path + 'HTFfeaturizedData', bucket, env_EMR)
            self.aws_infra.upload_processed_data(TFIDFfeaturizedData, path + 'TFIDFfeaturizedData', s3_path + 'TFIDFfeaturizedData', bucket, env_EMR)
            self.aws_infra.upload_processed_data(W2VfeaturizedData, path + 'W2VfeaturizedData', s3_path + 'W2VfeaturizedData', bucket, env_EMR)
        except:
            self.log.log_msg('[ERROR] Error saving the cleaned and transformed data', bucket = bucket)
            self.log.log_msg(traceback.format_exc(), bucket = bucket)
            spark.stop()
            raise Exception(traceback.format_exc())

        # log the success
        self.log.log_msg('[INFO] Data saved successfully', bucket = bucket)

        # log completion
        self.log.log_msg('[INFO] Preprocessing pipeline ran successfully', bucket = bucket)
        
        return HTFfeaturizedData, TFIDFfeaturizedData, W2VfeaturizedData