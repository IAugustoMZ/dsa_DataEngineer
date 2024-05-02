# !/bin/bash

# create docker image
docker build -t sstk-terraform-image:lab4 .

# create docker container
docker run -dit --name sstk-lab4 -v .\sstk_iac_deploy:/iac sstk-terraform-image:lab4 bin/bash

# run command in container
docker exec -it sstk-lab4 bin/bash