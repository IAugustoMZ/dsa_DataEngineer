# use official Ubuntu image
FROM ubuntu:latest

# maintainer
LABEL maintainer="SistekAnalytics"

# update and install necessary packages
RUN apt-get update && \
    apt-get install -y wget unzip curl openssh-client iputils-ping gnupg lsb-release

# define Terraform version
ENV TERRAFORM_VERSION=1.7.0

# download and install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# create the folder lab1 as volume
RUN mkdir /lab1
VOLUME /lab1

# add Google Cloud SDK repository and install
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && \
    apt-get install -y google-cloud-sdk

# define the entrypoint command
CMD ["/bin/bash"]