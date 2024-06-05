import os
import pendulum
import traceback

class LoggerClass:
    def __init__(self) -> None:
        """
        Constructor of the class LoggerClass
        for logging messages in the S3 bucket
        """
        # define the path of the log file
        self.path = "." if (os.path.isdir('logs')) else '/home/hadoop'

        # set suffix
        self.suffix = '-log-spark.txt'


    def log_msg(self, message: str, bucket: object=None) -> None:
        """
        Method to log messages in the S3 bucket

        Parameters
        ----------
        message : str
            The message to be logged
        bucket : object, optional
            S3 bucket object, by default None
        """
        # get the current date and time
        now_ = pendulum.now()

        # create file name
        file_name_date = now_.format('YYYYMMDD')

        # format the log datetime
        log_datetime = now_.format('YYYY-MM-DD HH:mm:ss')

        # create the complete path
        path = self.path + '/logs/' + file_name_date + self.suffix

        # create the message to be logged
        txt_msg = ''

        # tries to open the file in append mode if it exists, otherwise creates a new file
        try:
            # check if the file already exists
            if os.path.isfile(path):
                
                # open the file
                file = open(path, 'a')

                # add the message to the file
                txt_msg += '\n'

            else:
                # create the file
                file = open(path, 'w')
        # capture the exception
        except Exception as e:
            print('[ERROR] Error opening the log file')
            raise Exception(traceback.format_exc())
        
        # write the message in the file
        txt_msg += '[' + log_datetime + '] - ' + message

        # write the message in the file
        file.write(txt_msg)

        # close the file
        file.close()

        # check if the bucket is not None
        if bucket is not None:
            # upload the log file to the S3 bucket
            bucket.upload_file(path, 'logs/' + file_name_date + self.suffix)
        

