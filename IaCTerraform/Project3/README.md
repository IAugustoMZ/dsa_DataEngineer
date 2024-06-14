 # Data Engineer Formation - Project 3

## How to run the project

Follow these steps to run this project

1. In this project directory, run the docker compose command to build the image and start the container:

``docker-compose up --build``

2. After the building of the image has been completed, run the command to access the terminal inside the container

`docker exec -it sstk-proj3 bin/bash`

3. Once inside the container, download and install Azure CLI tool
`curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`

4. (Optional) Update the Azure CLI version

`az upgrade`

5. Log in in Azure

`az login`

6. Initialize Terraform inside the folder where the main.tf file is present

`terraform init`

7. (Optional) Validate the sintax of your Terraform files

`terraform validate`

8. Create the implementation plan

`terraform plan -out sstk.tfplan`

9. (Optional) Visualize the graph of dependencies for the infrastructure

`terraform graph`

10. Apply the implementation plan

`terraform apply sstk.tfplan`

11. After you finish work, destroy the provisioned infrastructure

`terraform destroy`

