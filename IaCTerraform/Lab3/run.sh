#/bin/bash

# create docker image
docker build -t sstk-terraform-image:lab3 .

# create docker container
docker run -dit --name sstk-lab3 -v ./tasks:/lab3 sstk-terraform-image:lab3 /bin/bash