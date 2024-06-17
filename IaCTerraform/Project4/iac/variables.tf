# prefix for the name of the resources
variable "name" {
    description = "Variable for prefixing the resource name"
    type        = string
    default     = "sstkp4-"
}

## Variables for AWS ------------------------------------------------------
# variable for CIDR - 1st public subnet
variable "aws_public_subnet_cidr_1" {
    type = string               
    description = "CIDR block for the first public subnet"  # variable description
    default     = "10.0.10.0/24"                            # standard value for CIDR block
}

# variable for CIDR - 2nd public subnet
variable "aws_public_subnet_cidr_2" {
    type = string               
    description = "CIDR block for the second public subnet"  # variable description
    default     = "10.0.11.0/24"                             # standard value for CIDR block
}

# variable for CIDR - 1st private subnet
variable "aws_private_subnet_cidr_1" {
    type = string               
    description = "CIDR block for the first private subnet"  # variable description
    default     = "10.0.20.0/24"                             # standard value for CIDR block
}

# variable for CIDR - 2nd public subnet
variable "aws_private_subnet_cidr_2" {
    type = string               
    description = "CIDR block for the second private subnet"  # variable description
    default     = "10.0.21.0/24"                              # standard value for CIDR block
}

# availability zone - 1st subnet in AWS
variable "aws_az_1" {
    type = string
    description = "Availability Zone for the first subnet"
    default = "us-east-1a"
}

# availability zone - 2nd subnet in AWS
variable "aws_az_2" {
    type = string
    description = "Availability Zone for the first subnet"
    default = "us-east-1b"
}

## Variables for Azure ------------------------------------------------------

# declaration of variables for location of Azure Resource Group
variable "resource_group_location" {
    type = string
    default = "eastus"
    description = "Resource Group location"
}