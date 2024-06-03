# script to implement the class to interact with
# AWS resources for the pipeline
import boto3

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