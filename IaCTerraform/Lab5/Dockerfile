# use official Ubuntu as a parent image
FROM ubuntu:latest

# maintainer
LABEL maintainer="Sistek Analytics"

# update all system packages and dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl openssh-client iputils-ping git

# define the Terraform version
ENV TERRAFORM_VERSION=1.6.5

# download and install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# create iac folder and set it as a volume
RUN mkdir /iac
VOLUME /iac

# create the downloads folder and install AWS CLI
RUN mkdir Downloads && \
    cd Downloads && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# standard command to run when the container starts
CMD ["/bin/bash"]