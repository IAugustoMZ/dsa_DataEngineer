#!/bin/bash
# script to build and run container

# create docker image
docker build -t sstk-terraform-image:lab2 .

# run docker container
docker run -dit --name sstk-lab2 sstk-terraform-image:lab2

# open shell in container
docker exec -it sstk-lab2 bin/bash