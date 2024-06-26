# Data Engineer Formation - Project 2

## How to run the project

Follow these steps to run this project:

1. In this project directory, run the docker compose command to build the image and start the container:

``docker-compose up --build``

2. After the building of the image has been completed, run the command to access the terminal inside the container

`docker exec -it sstk-proj2 bin/bash`

3. Once inside the container, run the command to configure the AWS cloud credentials

`aws configure`

4. Edit the files `config.tf` and `terraform.tfvars` and put your ID from AWS where necessary

5. At the script `aws_infra.py`, add your AWS ID and the AWS keys where necessary.

6. Manually create a bucket named `sstk-p2-terraform-<your-aws_id>`

7. In the `iac/iac` folder inside the container, run:

```terraform init``

8. Create the Terraform plan and save it in the disk

`terraform plan`

8. Apply  the changes using one of the following:

`terraform apply -auto-approve -var-file config.tfvars`
`terraform apply -var-file config.tfvars`

9. Follow the pipeline execution through the AWS interface as showed.

10. After finishing the jobs, you can destroy the cluster

`terraform plan -destroy -var-file config.tfvars -out terraform.tfplan`

11. Apply the destroy plan

`terraform apply terraform.tfplan`