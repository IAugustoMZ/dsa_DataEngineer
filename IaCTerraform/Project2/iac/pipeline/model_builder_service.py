from aws_infra import AWSInfra
from proj_log import LoggerClass
from pyspark.ml.feature import *
from pyspark.sql import functions
from pyspark.sql.functions import *
from pyspark.ml.evaluation import *
from pyspark.ml.classification import *
from pyspark.sql.types import StringType, IntegerType
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

class SparkModelBuilder:

    def __init__(self) -> None:
        """
        Constructor for the class SparkModelBuilder to create
        the machine learning models
        """
        # instantiate log
        self.log = LoggerClass()

        # instantiate the AWSInfra class
        self.aws_infra = AWSInfra()

    def run(self, spark: object, bucket: object, bucket_name: str, env_EMR: bool,
            data_list: list) -> None:
        """
        Method to run the modeling pipeline

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
        data_list : list
            list with the featurized datasets
        """
        # list of classifiers
        classifiers = [LogisticRegression(), RandomForestClassifier(), GBTClassifier()]

        # loop through the list of datasets
        for data in data_list:

            # log the message
            self.log.log_msg(data.name + " Results: ", bucket)

            # split the data into training and testing
            train_data, test_data = data.randomSplit([0.7, 0.3], seed=42)

            # fit MinMaxScaler on train data
            scaler = MinMaxScaler(inputCol="features", outputCol="scaledFeatures")
            scalerModel = scaler.fit(train_data)

            # transform train and test data
            train_data_scaled = scalerModel.transform(train_data)
            test_data_scaled = scalerModel.transform(test_data)

            # change the attributes names
            train_data_scaled.name = data.name
            train_data_scaled = train_data_scaled.select("class", "scaledFeatures")
            train_data_scaled = train_data_scaled.withColumnRenamed("scaledFeatures", "features")
            test_data_scaled = test_data_scaled.select("class", "scaledFeatures")
            test_data_scaled = test_data_scaled.withColumnRenamed("scaledFeatures", "features")

            # get x and y
            x = data.select(["features"]).collect()
            y = data.select("class").distinct().count()

            # create the columns list
            columns = ["Classifier", "Result"]

            # create the values list
            vals = [("Place Holder", "N/A")]

            # create the dataframe
            results = spark.createDataFrame(vals, columns)

            # loop through the list of classifiers
            for classifier in classifiers:

                # create the object of the class
                new_result = self.train_eval_model(
                    spark, classifier, x, y, train_data_scaled, test_data_scaled,
                    bucket, bucket_name, env_EMR
                )

                # generate the result
                results = results.union(new_result)
                results = results.where("Classifier!='Place Holder'")
    
    def train_eval_model(self,
                         spark: object,
                         classifier: object,
                         x: object,
                         y: int,
                         train_data: object,
                         test_data: object,
                         bucket: object,
                         bucket_name: str,
                         env_EMR: bool) -> object:
            """
            Method to train and evaluate the model
    
            Parameters
            ----------
            spark : object
                Spark session object
            classifier : object
                classifier object
            x : object
                features
            y : int
                number of classes
            train_data : object
                training data
            test_data : object
                testing data
            bucket : object
                AWS Bucket object
            bucket_name : str
                name of the bucket
            env_EMR : bool
                flag to indicate if the environment is Amazon EMR
    
            Returns
            -------
            object
                dataframe with the results
            """
            # create the model instance
            Mtype = self.FindMtype(classifier)

            # fit the model
            fitModel = self.InstanceFitModel(Mtype, classifier, x, y, train_data)

            # evaluate the model
            if fitModel is not None:
                
                # log the best model
                self.log.log_msg('[INFO] Best model: ' + str(fitModel.bestModel), bucket)

                # column names to compare metrics
                columns = ["Classifier", "Result"]

                # make predictions
                predictions = fitModel.transform(test_data)

                # create the evaluator
                MC_evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

                # calculate the accuracy
                accuracy = (MC_evaluator.evaluate(predictions)) * 100

                # log the accuracy
                self.log.log_msg("Classifier: " + Mtype + " / Accuracy: " + str(accuracy), bucket)
                
                # values to compare metrics
                Mtype = [Mtype]
                score = [str(accuracy)]
                result = spark.createDataFrame(zip(Mtype, score), schema=columns)
                result = result.withColumn("Result", result.Result.substr(0, 5))

                # path to save the result
                path = (f"s3://{bucket_name}/output/" + Mtype[0] + '_' + 
                        train_data.name if env_EMR else 'output/' + Mtype[0] + '_' + train_data.name)
                s3_path = 'output/' + Mtype[0] + '_' + train_data.name

                # save the result to the bucket
                self.aws_infra.upload_ml_model(fitModel, path, s3_path, bucket, env_EMR)

                return result

    @staticmethod
    def FindMtype(classifier: object) -> str:
        """
        Method to find the model type

        Parameters
        ----------
        classifier : object
            classifier object

        Returns
        -------
        str
            model type
        """
        return type(classifier).__name__
    
    @staticmethod
    def InstanceFitModel(Mtype: str, classifier: object, x: object, y: int, train_data: object) -> object:
        """
        Method to fit the model

        Parameters
        ----------
        Mtype : str
            model type
        classifier : object
            classifier object
        x : object
            features
        y : int
            number of classes
        train_data : object
            training data

        Returns
        -------
        object
            fitted model
        """
        if Mtype in ("LogisticRegression"):

            # create the grid of hyperparameters
            paramGrid = (ParamGridBuilder().addGrid(classifier.maxIter, [10, 15, 20]).build())

            
        elif Mtype in ("RandomForestClassifier"):

            # create the grid of hyperparameters
            paramGrid = (ParamGridBuilder()
                         .addGrid(classifier.maxDepth, [5, 10, 15])
                         .addGrid(classifier.numTrees, [50, 100, 150])
                         .build())
            
        elif Mtype in ("GBTClassifier"):

            # create the grid of hyperparameters
            paramGrid = (ParamGridBuilder()
                         .addGrid(classifier.maxDepth, [5, 10, 15])
                         .addGrid(classifier.maxIter, [10, 15, 20])
                         .addGrid(classifier.stepSize, [0.1, 0.2, 0.3])
                         .build())

        # create the cross validator
        crossval = CrossValidator(estimator=classifier,
                                    estimatorParamMaps=paramGrid,
                                    evaluator=MulticlassClassificationEvaluator(),
                                    numFolds=5)

        # fit the model
        fitModel = crossval.fit(train_data)

        return fitModel

            