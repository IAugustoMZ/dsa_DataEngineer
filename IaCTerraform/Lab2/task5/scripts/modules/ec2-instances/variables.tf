variable "instance_count" {
    description = "Number of instances EC2 to be created"
    type        = number
}

variable "ami_id" {
    description = "AMI ID for EC2 instances"
    type        = string
}

variable "instance_type" {
    description = "Instance type for EC2 instances"
    type        = string
}

variable "subnet_id" {
    description = "Subnet ID for EC2 instances"
    type        = string
}
