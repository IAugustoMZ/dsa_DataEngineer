variable "region" {
    description = "The region in which the resources will be created"
    type        = string
    default     = "us-east-2"
}

variable "instance_type" {
    description = "The type of EC2 instance to create"
    type        = string
    default     = "t2.micro"
}

variable "vpc_ids" {
    description = "VPCs IDs to create the EC2 instance in"
    type        = list(string)
}

variable subnets {
    description = "Subnets IDs to create the EC2 instance in"
    type        = list(string)
}

variable "ami_id" {
    description = "AMI ID for EC2"
    type        = string
}