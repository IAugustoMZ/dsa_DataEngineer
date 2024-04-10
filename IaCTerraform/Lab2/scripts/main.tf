variable "instance_type" {
    description = "The type of the instance to be created"
}

variable "ami" {
    description = "Amazon Machine Image to be used"
}

variable "region" {
    description = "The region in which the instance will be created"
    default = "us-east-2"
}

provider "aws" {
    region = var.region
}

resource "aws_instance" "sstk_ec2" {
    ami           = var.ami
    instance_type = var.instance_type
    tags = {
        Name = "SSTK-EC2-terraform"
    }
}