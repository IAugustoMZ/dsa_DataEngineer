# usando imagem Ubuntu
FROM ubuntu:latest

# nomeando mantenedor da imagem
LABEL maintainer="sistek_analytics"

# atualizando pacotes do sistema e instalando pacotes necessários
RUN apt-get update && \
    apt-get install -y wget unzip curl

# definir a versão do Terraform
ENV TERRAFORM_VERSION=1.6.2

# baixar o Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# criar a pasta lab1 dentro do container
RUN mkdir /lab1

# copiar o arquivo main.tf para a pasta lab1
COPY main.tf /lab1/

# criar a pasta downloads e instalar o AWS CLI
RUN mkdir /downloads && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/downloads/awscliv2.zip" && \
    unzip /downloads/awscliv2.zip -d /downloads && \
    /downloads/aws/install

# definir o comando de execução quando o container for iniciado
CMD [ "/bin/bash" ]