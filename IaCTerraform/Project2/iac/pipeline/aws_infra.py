# script to implement the class to interact with
# AWS resources for the pipeline
import boto3
from proj_log import LoggerClass

class AWSInfra:

    BUCKET_NAME     = "sstk-p2-574973852419"
    AWSACCESSKEYID  = "put-here-your-aws-access-key-id"
    AWSSECRETKEY    = "put-here-your-aws-secret-key"

    def __init__(self):
        """
        Constructor for the class AWSInfra, which allows
        interaction with AWS resources
        """
        
        # resource to access S3 via Python
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=self.AWSACCESSKEYID,
            aws_secret_access_key=self.AWSSECRETKEY
        )

        # logger
        self.logger = LoggerClass()

    def get_bucket(self, bucket_name: str = None) -> object:
        """
        Method to get the bucket from the AWS S3

        Parameters
        ----------
        bucket_name : str, optional
            name of the bucket, by default None

        Returns
        -------
        object
            AWS Bucket object
        """

        if bucket_name is None:
            bucket_name = self.BUCKET_NAME
        # access to the S3 bucket
        bucket = self.s3_resource.Bucket(bucket_name)
        return bucket
    
    def upload_processed_data(self,
                              data: object,
                              path: str,
                              s3_path: str,
                              bucket: object,
                              env_EMR: bool = False) -> None:
        """
        Method to upload the processed data to the S3 bucket

        Parameters
        ----------
        data : object
            data to be uploaded
        path : str
            path to the data
        s3_path : str
            path to the data in the S3 bucket
        bucket : object
            AWS Bucket object
        env_EMR : bool, optional
            flag to indicate if the environment is Amazon EMR, by default False
        """
        # check if the function is being executed in Amazon EMR
        if env_EMR:
            # check if there is already any object in the S3 bucket
            if len(list(bucket.objects.filter(Prefix=s3_path)).limit(1)) > 0:
                # if there is, overwrite it
                data.write.mode("Overwrite").partitionBy('class').parquet(path)
            else:
                # if there is not, create a new object
                data.write.partitionBy('class').parquet(path)
        else:
            # log the error of not being in Amazon EMR
            self.logger.log_msg('[ERROR] Environment is not Amazon EMR')

    def upload_ml_model(self,
                        model: object,
                        path: str,
                        s3_path: str,
                        bucket: object,
                        env_EMR: bool = False) -> None:
        """
        Method to upload the ML model to the S3 bucket

        Parameters
        ----------
        model : object
            ML model to be uploaded
        path : str
            path to the model
        s3_path : str
            path to the model in the S3 bucket
        bucket : object
            AWS Bucket object
        env_EMR : bool, optional
            flag to indicate if the environment is Amazon EMR,
            by default False
        """
        # check if the function is being executed in Amazon EMR
        if env_EMR:
            # check if there is already any object in the S3 bucket
            if len(list(bucket.objects.filter(Prefix=s3_path)).limit(1)) > 0:
                # if there is, overwrite it
                model.write().overwrite().save(path)
            else:
                # if there is not, create a new object
                model.write().save(path)
        else:
            # log the error of not being in Amazon EMR
            self.logger.log_msg('[ERROR] Environment is not Amazon EMR')