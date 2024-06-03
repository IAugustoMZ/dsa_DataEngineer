from preprocessing_service import SparkPreprocessor
from model_builder_service import SparkModelBuilder

class SafetyReportCompletePipeline:

    def __init__(self,
                 spark_session: object,
                 aws_bucket: object,
                 bucket_name: str,
                 environment_EMR: bool) -> None:
        """
        Constructor for the class SafetyReportCompletePipeline, which
        contains the complete pipeline for the project that preprocesses and train
        machine learning models to predict the criticity of a safety report

        Parameters
        ----------
        spark_session : object
            Spark session object
        aws_bucket : object
            AWS Bucket object
        bucket_name : str
            name of the bucket
        environment_EMR : bool
            flag to indicate if the environment is Amazon EMR
        """
        self.spark_session = spark_session
        self.aws_bucket = aws_bucket
        self.bucket_name = bucket_name
        self.environment_EMR = environment_EMR

        # instantiate the SparkPreprocessor class
        spark_preprocessor = SparkPreprocessor()

        # instantiate the SparkModelBuilder class
        spark_model_builder = SparkModelBuilder()

    def run_preprocessing(self) -> list:
        """
        Method to run the preprocessing pipeline

        Returns
        -------
        list
            list with the featurized datasets
        """
        # run preprocessing pipeline
        DataHTFfeaturized, DataTFIDFfeaturized, DataW2Vfeaturized = self.spark_preprocessor.run(
            spark=self.spark_session,
            bucket=self.aws_bucket,
            bucket_name=self.bucket_name,
            env_EMR=self.environment_EMR
        )

        return [DataHTFfeaturized, DataTFIDFfeaturized, DataW2Vfeaturized]
    
    def run_modeling(self, dataset_list: list) -> None:
        """
        Method to run the modeling pipeline

        Parameters
        ----------
        dataset_list : list
            list with the featurized datasets
        """
        # run modeling pipeline
        self.spark_model_builder.run(
            spark=self.spark_session,
            bucket=self.aws_bucket,
            bucket_name=self.bucket_name,
            env_EMR=self.environment_EMR,
            dataset_list=dataset_list
        )

    
