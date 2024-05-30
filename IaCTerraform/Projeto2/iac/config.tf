# remote state configuration, Terraform version and provider

terraform {
    required_version = "~> 1.7"

    # provider AWS
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }

    # backend used for remote state
    backend "s3" {
        encrypt = true
        bucket  = var.name_bucket_state
        key     = "sstk-p2.tfstate"
        region  = var.region
    }
}

# provider AWS region
provider "aws" {
    region = var.region
}