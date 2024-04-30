variable "instance_type" {
    description = "The type of EC2 instance to create"
    type        = list(string)
}

variable "ami_id" {
    description = "AMI ID for EC2"
    type        = list(string)
}