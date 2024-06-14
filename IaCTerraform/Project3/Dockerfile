# use official ubuntu image as base image
FROM ubuntu:latest

# maintainer
LABEL maintainer="SistekAnalytics"

# update the package repository and install necessary dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl git sudo openssh-client iputils-ping

# define Terraform version
ENV TERRAFORM_VERSION=1.8.2

# download and install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# create the folder /iac as volume mount
RUN mkdir /iac
VOLUME /iac

# define the command to run when the container starts
CMD ["/bin/bash"]
