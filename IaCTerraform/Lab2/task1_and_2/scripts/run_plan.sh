#!/bin/bash
# script to run terraform plan and save the plan to a file

# terraform run script
terraform init

# check the plan
terraform plan -var-file "variables.tfvars" -out lab2-plan.txt
