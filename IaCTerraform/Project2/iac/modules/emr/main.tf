# provisioning the EMR cluster

# resource for the creation of the cluster EMR
resource "aws_emr_cluster" "cluster" {

    # name of the cluter
    name = var.name_emr

    # version
    release_label = "emr-7.0.0"

    # applications
    applications = ["Hadoop", "Spark"]

    # protection against cluster termination
    termination_protection = false

    # keep the processing job active
    keep_job_flow_alive_when_no_steps = false

    # URI with the folders for logs
    log_uri = "s3://${var.name_bucket}/logs"

    # service role IAM
    service_role = var.service_role

    # attributes of the EC2 instances of the cluster
    ec2_attributes {
      instance_profile = var.instance_profile
      emr_managed_master_security_group = aws_security_group.main_security_group.id
      emr_managed_slave_security_group = aws_security_group.core_security_group.id
    }

    # type of instances of cluster
    master_instance_group {
      instance_type = "m5.4xlarge"
    }

    # type of instances of workers
    core_instance_group {
      instance_type = "m5.2xlarge"
      instance_count = "2"
    }

    # executes the installation script for Python interpreter and additional packages
    bootstrap_action {
      name = "Install additional Python packages"
      path = "s3://${var.name_bucket}/bootstrap.sh"
    }

    # steps executed in the cluster
    # 1 - copy the files from S3 to the EC2 for the cluster. If it fails, the cluster is terminated
    # 2 - copy the log files from the S3 to the EC2 instances of the cluster. If it fails, the cluster
    # is terminated
    # 3 - runs the Python script for the job processing. If it fails, the cluster is kept alive to allow
    # investigation of the failure 
    step = [
        {
            name                = "Copy scripts to EC2 instances"
            action_on_failure   = "TERMINATE_CLUSTER"
            hadoop_jar_step = [
                {
                    jar         = "command-runner.jar"
                    args        = ["aws", "s3", "cp", "s3://${var.name_bucket}/pipeline", "/home/hadoop/pipeline", "--recursive"]
                    main_class  = ""
                    properties  = {}
                }
            ]
        },
        {
            name                = "Copy log files to EC2"
            action_on_failure   = "TERMINATE_CLUSTER"

            hadoop_jar_step = [
              {
                jar         = "command-runner.jar"
                args        = ["aws", "s3", "cp", "s3://${var.name_bucket}/logs", "/home/hadoop/logs", "--recursive"]
                main_class  = ""
                properties  = {}
              }
            ]
        },
        {
            name                = "Run Python script"
            action_on_failure   = "CONTINUE"

            hadoop_jar_step = [
              {
                jar         = "command-runner.jar"
                args        = ["spark-submit", "s3://${var.name_bucket}/pipeline/main_project2.py"]
                main_class  = ""
                properties  = {}
              }
            ]
        }
    ]

    # Spark configuration file
    configurations_json = <<EOF
    [
      {
        "Classification": "spark-defaults",
        "Properties": {
          "spark.pyspark.python": "/home/hadoop/conda/bin/python",
          "spark.dynamicAllocation.enabled": "true",
          "spark.network.timeout": "800s",
          "spark.executor.heartbeatInterval": "60s",
        }
      }
    ]
    EOF
}