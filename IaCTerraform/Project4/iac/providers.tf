# providers file - Deploy Multi Cloud

# configuration of the terraform version to execute the
# script
terraform {
    required_version = ">= 1.6"

    # necessary providers
    required_providers {
        # defines the Azure RM and the minimum version required
        azurerm = {
            source  = "hashicorp/azurerm"
            version = ">= 3.99.0" 
        }

        # deifnes the provider AWS and the minimum required version
        aws = {
            source  = "hashicorp/aws"
            version = ">= 5.45.0"
        }
    }
}

# configures the Azure Resource Manager
provider "azurerm" {
    features = {} # needed, but without specific features
}

# configures the AWS provider
provider "aws" {
    region = "us-east-1"    # region of the provider
}