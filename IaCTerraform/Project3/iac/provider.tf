# configuration of Terraform
terraform {
    # required providers
    required_providers {

        # provider AzureRm da HashiCorp
        azurerm = {

            # source and version
            source  = "hashicorp/azurerm"
            version = "~> 3.0"
        }
    }
}

# AzureRM provider configuration
provider "azurerm" {
    # standard features and functionalities
    features {}
}