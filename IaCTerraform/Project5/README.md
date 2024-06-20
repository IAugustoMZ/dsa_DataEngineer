# Data Engineer Formation - Project 5

## How to run the project

Follow these steps to run this project

1. In this project directory, run the docker compose command to build the image and start the container:

``docker-compose up --build``

2. After the building of the image has been completed, run the command to access the terminal inside the container

`docker exec -it sstk-proj5 bin/bash`

3. Once inside the container, run the command to download and install Databricks CLI

`curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh`

4. Configure the authentication

`databricks configure --token`

