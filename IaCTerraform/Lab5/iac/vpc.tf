# define the virtual private network
module "vpc" {
    source = "terraform-aws-modules/vpc/aws"        # use this module as reference
    version = "5.4.0"

    # name of the VPC and CIDR block
    name = "ecs-vpc"
    cidr = var.vpc_cidr_block       # IP range for the VPC

    # availability zones and subnets
    azs                  = [ var.avail_zone1, var.avail_zone2 ]
    public_subnets       = [ var.public_subnet_1_cidr_block, var.public_subnet_2_cidr_block ]
    private_subnets      = [ var.private_subnet_1_cidr_block ]

    # tag for each resource in the VPC
    private_subnet_tags         = { Name = "${var.project_name}-${var.environment}-private-subnet" }
    public_subnet_tags          = { Name = "${var.project_name}-${var.environment}-public-subnet" }
    igw_tags                    = { Name = "${var.project_name}-${var.environment}-igw" }
    default_security_group_tags = { Name = "${var.project_name}-${var.environment}-default-sg" }
    default_route_table_tags    = { Name = "${var.project_name}-${var.environment}-default-rtb" }
    public_route_table_tags     = { Name = "${var.project_name}-${var.environment}-public-rtb" }

    # tag for the VPC
    vpc_tags = { Name = "${var.project_name}-${var.environment}-vpc" }
}