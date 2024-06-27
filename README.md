# Formation Data Engineer - Data Science Academy

<br>


This repository contains the practical laboratories of the Data Engineer formation from Data Science Academy

## 🐋 Docker and Kubernetes

This part has the scripts and codes used in the practical activities of the Linux, Docker and Kubernetes course

- Linux Basic Commands
- Automation with Bash scripting
- Docker
- Docker Compose
- Kubernetes

## 📊 EGovAnalytics

This folder contains the project developed of Exploratory Data Analysis for E-Gov information.

Here, we tried to correlate the Gross Domestic Product with the amount spent in Public Health and Education. In addition, we tried to come up with recomendations for governments to act upon such relationship.

## ☁️ Infrastructure as Code with Terraform, AWS, Azure and Databricks

The first course of the Data Engineer formation includes the automation procedures to provision cloud infrastructure using Terraform to manage and orchestrate.

- **Laboratory 1** - Provision of Amazon EC2 instance using Terraform
- **Laboratory 2** - Provision of Amazon EC2 instance using Terraform using:
    - *Entry variables* - definition of a variable plan to hold all necessary variables for the infrastructure
    - *Terraform Plan* - creation of the infrastructure plan, and saving it into a file
    - *Mutiple Subnets* - provision of multiple EC2 instances in different subnets
    - *Concept of Modules* - presentation of modularization concept for different infrastructure provision in a reusable form
        - Deploy of two EC2 instances in the same resource module
        - Deploy of two EC2 instances and one S3 bucket in different modules
    - *Terraform Output* - use of output files to capture variables sent by AWS after Terraform application.
- **Laboratory 3** - Provision of Amazon EC2 instance using Provisioners
    - *Provisioners* - implementation of a web server by executing commands inside and outside the provisioned EC2 instance using the Provisioners feature.
    - *Security Groups* - automated the creation and configuration of security groups with Terraform
    - *Using Shell Scripts* - automated the execution of shell (bash) scripts inside the EC2 instance
    - *Without Provisioners* - executed shell (bash) scripts inside the EC2 instance without the use of Provisioners
    - *Multiple instances with checking* - the script used repetitions and conditionals expressions to automate the creation of multiple web servers with type validation
- **Laboratory 4** - Provision of an entire infrastructure (EC2 + S3) to serve a machine learning model web application
    - *Provisioners* - to run delete commands when destroying IaC
    - *Machine Learning Model Training and Deploy* - using classic Data Science and Machine Learning techniques
    - *Web Application Development* - to serve the model predictions and to allow user inputs and interactions
- **Laboratory 5** - Provision of a complete application served by a Docker container
    - *Amazon Elastic Container Services* - for supporting the execution of the containers
    - *Amazon Application Load Balancer* - to balance the load across server replics
    - *VPCs, security groups and IAM roles* - to manage privileges and access
    - *Docker-Compose* - to ease the creation of the container (client)
- **Project 1** - Provision of an EMR (Amazon Elastic Map Reduce) cluster to process data
    - build the Terraform infrastructure scripts
    - run the infrastructure using Docker-Compose + Linux commands
    - run a data processing job using Apache Flink - WordCount example
- **Project 2** - Provision of an EMR cluster (Amazon Elastic Map Reduce) to train a machine learning model
    - Terraform infrastructure
    - all the model training and evaluation was made through Terraform automation and Apache Spark commands
    - the problem is to create a NLP model that automatically classifies the gravity of a text report referring safety incidents and accidents.
- **Project 3** - Basic provision of virtual machines in Microsoft Azure cloud
- **Project 4** - Basic provision of virtual machines in Microsoft Azure cloud and AWS using the advantages of multi-cloud services
- **Project 5** - Provision and execution of infrastructure in Databricks Cloud using Terraform - WIP 🚧

## 📈 Database Analytics Using DuckDB

In this course, it is shown how to use DuckDB as a local columnar database along with SQL expressions to query data for insights.

- **Project** - implementation of an ETL flow to extract data from a production and quality huge table, transform them into a star schema model and load them into a DuckDB table.
    - After the ETL job, we perform some queries to gain insights about the quality and process status of this industry.
    - 🚧 Work in Progress
