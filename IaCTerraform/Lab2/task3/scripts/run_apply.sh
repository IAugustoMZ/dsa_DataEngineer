#!/bin/bash
# script to apply the infrastructure

# apply the infrastructure
terraform apply -var-file "variables.tfvars" -auto-approve
