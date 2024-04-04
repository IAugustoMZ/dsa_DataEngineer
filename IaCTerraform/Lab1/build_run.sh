# create docker image
docker build -t sstk-terraform-image:lab1 .

# run docker container
docker run -dit --name sstk-lab1 sstk-terraform-image:lab1

# open shell in container
docker exec -it sstk-lab1 bin/bash