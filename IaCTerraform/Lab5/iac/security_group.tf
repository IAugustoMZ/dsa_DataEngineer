# define the security group for the ECS cluster
module "container-security-group" {
    source  = "terraform-aws-modules/security-group/aws"
    version = "5.1.0"

    # defines the name of the security group and binds it to
    # the VPC
    # this is the security group of the ECS container
    name    = "${var.project_name}-${var.environment}-ecs-sg"
    vpc_id  = module.vpc.vpc_id

    # defines the ingress rules for the security group
    ingress_with_cidr_blocks = [
        {
            from_port   = var.container_port
            to_port     = var.container_port
            protocol    = "tcp"
            description = "container security group ingress rule"
            cidr_blocks = "0.0.0.0/0"
        }
    ]

    # defines the egress rules for the security group
    egress_rules = [ "all-all" ]

    # tag for the security group
    tags = { Name = "${var.project_name}-${var.environment}-ecs-sg" }
}

# define the security group for the Application Load Balancer
module "alb-security-group" {
    source  = "terraform-aws-modules/security-group/aws"
    version = "5.1.0"

    # defines the name of the security group and binds it to
    # the VPC
    # this is the security group of the Application Load Balancer
    name    = "${var.project_name}-${var.environment}-alb-sg"
    vpc_id  = module.vpc.vpc_id

    # defines the ingress rules for the security group
    ingress_cidr_blocks = [
        {
            from_port   = var.alb_sg_port
            to_port     = var.alb_sg_port
            protocol    = "tcp"
            description = "ALB security group ingress rule"
            cidr_blocks = "0.0.0.0/0"
        }
    ]

    # defines the egress rules for the security group
    egress_rules = [ "all-all" ]

    # tag for the security group
    tags = { Name = "${var.project_name}-${var.environment}-alb-sg" }
}
