# use ubuntu as base image
FROM ubuntu:latest

# maintainer
LABEL maintainer="Sistek Analytics"

# update the package repository
RUN apt-get update && \
    apt-get install -y wget unzip curl openssh-client iputils-ping

# define Terraform version
ENV TERRAFORM_VERSION=1.6.4

# download and install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# create the folder lab3 as a volume
RUN mkdir /lab3
VOLUME /lab3/

# create the folder downlodas and install AWS CLI
RUN mkdir /downloads && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/downloads/awscliv2.zip" && \
    unzip /downloads/awscliv2.zip -d /downloads && \
    /downloads/aws/install

# default command to run when the container starts
CMD ["/bin/bash"]