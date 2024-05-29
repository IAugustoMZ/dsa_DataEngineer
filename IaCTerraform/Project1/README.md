# Data Engineer Formation - Project 1

## How to run the project

Follow these steps to run this project

1. In this project directory, run the docker compose command to build the image and start the container:

``docker-compose up --build``

2. After the building of the image has been completed, run the command to access the terminal inside the container

`docker exec -it sstk-proj1 bin/bash`

3. Once inside the container, run the command to configure the AWS cloud credentials

`aws configure`

4. Create an Amazon S3 bucket with the name sstk-p1-<account_id> and configure it in the file `emr.tf`

5. In the `iac` folder inside the container, run:

```terraform init``

6. Create the Terraform plan and save it in the disk

`terraform plan -var-file config.tfvars -out terraform.tfplan`

7. Apply  the changes using one of the following:

`terraform apply -auto-approve -var-file config.tfvars`
`terraform apply -var-file config.tfvars`

8. Go to the `generated/ssh` folder and change the private key privilege (read-only)

`chmod 400 deployer`

9. Run the SSH access command (note that the username changes depending on the EMR DNS address)

`ssh -i deployer hadoop@ec2-18-224-137-192.us-east-2.compute.amazonaws.com`

10. After you successfully connect to the master node (via SSH or via browser), create a folder in the HDFS

`hdfs dfs -mkdir /user/root/input`

11. Copy the file `dados.txt` to the HDFS

`hdfs dfs -put dados.txt /user/root/input`

12. You can count the number of occurrences of each word in the file using the Apache Flink

`flink run -m yarn-cluster /usr/lib/flink/examples/streaming/WordCount.jar --input hdfs:///user/root/input/dados.txt --output hdfs:///user/root/output/`

13. You can access the HDFS file using:

`hdfs dfs -get /user/root/output/2024-05-28--00`

14. You can add a step in the cluster by running:

`aws emr add-steps --cluster-id j-2NEZMXP20K2OK --steps Type=CUSTOM_JAR,Name=job1_p1,Jar=command-runner.jar,Args="flink","run","-m","yarn-cluster","/usr/lib/flink/examples/streaming/WordCount.jar","--input","hdfs:///user/root/input/dados.txt","--output","hdfs:///user/root/outputjob1/" --region us-east-2`

15. An alternative is to run the same job, but reading from and writing to the Amazon S3 service

`aws emr add-steps --cluster-id j-2QLSX6UWLP59U --steps Type=CUSTOM_JAR,Name=job1_p1,Jar=command-runner.jar,Args="flink","run","-m","yarn-cluster","/usr/lib/flink/examples/streaming/WordCount.jar","--input","s3://sstk-p1-574973852419/pneumatic_valve.txt","--output","s3://sstk-p1-574973852419/word_count_valve_manual.txt" --region us-east-2`

16. After finishing the jobs, you can destroy the cluster

`terraform plan -destroy -var-file config.tfvars -out terraform.tfplan`

17. Apply the destroy plan

`terraform apply terraform.tfplan`