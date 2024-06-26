# use the official Python image as base image
FROM python:3.12

# image maintainer
LABEL maintainer="SistekAnalytics"

# updates the mirrors list and install additional packages
RUN apt-get update && \
    apt-get install -y wget unzip curl git sudo iputils-ping

# defines the working directory
WORKDIR /

# copy the requirements file into the container
# and install the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# creta the folders for volume mount
RUN mkdir /duckdb_intro
VOLUME /duckdb_intro

RUN mkdir /duckdb_project
VOLUME /duckdb_project

# defines the command to run when the container starts
CMD ["/bin/bash"]