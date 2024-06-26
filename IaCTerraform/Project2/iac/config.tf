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
        bucket  = "sstk-p2-terraform-574973852419"
        key     = "sstk-p2.tfstate"
        region  = "us-east-2"
    }
}

# provider AWS region
provider "aws" {
    region = "us-east-2"
}