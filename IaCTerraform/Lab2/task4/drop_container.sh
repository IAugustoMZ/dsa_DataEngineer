#!/bin/bash
# script to drop container and image

# stop running container
docker stop sstk-lab2-t3

# remove container
docker rm sstk-lab2-t3

# remove image
docker rmi sstk-terraform-image:lab2-t4