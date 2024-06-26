# use an official Ubuntu image
FROM ubuntu:latest

# maintainer
LABEL maintainer="SistekAnalytics"

# update the package list and install the necessary dependencies
RUN apt-get update && \
    apt-get install -y wget unzip curl git openssh-client iputils-ping

# defin Terraform version
ENV TERRAFORM_VERSION=1.7.4

# download and install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# create the folder as a volume mount
RUN mkdir /iac
VOLUME /iac

# create the folder downloads and install AWS CLI
RUN mkdir /downloads && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/downloads/awscliv2.zip" && \
    unzip /downloads/awscliv2.zip -d /downloads && \
    /downloads/aws/install

# define the standard command when the container starts
CMD ["/bin/bash"]