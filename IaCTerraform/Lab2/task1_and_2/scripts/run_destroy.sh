#!/bin/bash
# script to destroy the infrastructure

# check the plan
terraform destroy -var-file "variables.tfvars" -auto-approve
