# script to define a provider
terraform {
    required_providers {
        databricks = {
            source = "databricks/databricks"
        }
    }
}