# defining VPCs and Subnets

# variable for the region
variable "region" {
  description = "The region in which the VPC will be created"
  default     = "us-west-2"
  type        = string
}

# tags
variable "tags" {}

# create the VPC with two subnets
module "vpc" {
    source                  = "terraform-aws-modules/vpc/aws"
    name                    = "sstk-core"
    cidr                    = "10.0.0.0/16"
    azs                     = [lookup(var.az_zone_a, var.region), lookup(var.az_zone_b, var.region)]
    public_subnets          = ["10.0.0.0/24", "10.0.2.0/24"]
    enable_dns_support      = true
    enable_dns_hostnames    = true
    enable_nat_gateway      = false
    map_public_ip_on_launch = true
    tags                    = var.tags
}

# create a security group to integrate services inside the VPC
resource "aws_security_group" "integration-service-security-group" {
  name        = "integration-service-security-group"
  description = "Security group for integration services - allow inbound traffic in the VPC"
  vpc_id      = module.vpc.vpc_id
  tags        = var.tags
}

# outputs
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_1" {
  value = module.vpc.public_subnets[0]
}

output "public_subnet_2" {
  value = module.vpc.public_subnets[1]
}

output "integration_service_security_group_id" {
  value = aws_security_group.integration-service-security-group.id
}