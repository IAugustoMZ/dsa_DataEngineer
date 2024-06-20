# defines a VPC in AWS with a block CIDR
resource "aws_vpc" "aws_sstk_vpc" {
    cidr_block = "10.0.0.0/16"

    tags = {
        Name = "${var.name}_vpc"
    }
}

# defines the first public subnet in AWS
resource "aws_subnet" "aws_public_subnet_1" {
    vpc_id              = aws_vpc.aws_sstk_vpc.id
    cidr_block          = var.aws_public_subnet_cidr_1
    availability_zone   = var.aws_az_1

    tags = {
        Name = "${var.name}_public_subnet_1"
    }
}

# defines the second public subnet in AWS
resource "aws_subnet" "aws_public_subnet_2" {
    vpc_id              = aws_vpc.aws_sstk_vpc.id
    cidr_block          = var.aws_public_subnet_cidr_2
    availability_zone   = var.aws_az_2

    tags = {
        Name = "${var.name}_public_subnet_2"
    }
}

# defines an internet gateway for the VPC
resource "aws_internet_gateway" "aws_ig" {
    vpc_id = aws_vpc.aws_sstk_vpc.id

    tags = {
        Name = "${var.name}_ig"
    }
}

# defines a routing table for the public subnets
resource "aws_route_table" "aws_pub_rt" {
    vpc_id = aws_vpc.aws_sstk_vpc.id    # relates routing table to VPC

    route {
        cidr_block = "0.0.0.0/0"        # all internet traffic to gateway
        gateway_id = aws_internet_gateway.aws_ig.id
    }

    tags = {
        Name = "${var.name}_pub_rt"
    }
}

# associates the first public subnet to the routing table
resource "aws_route_table_association" "aws_pub_sub_assoc_1" {
    subnet_id       = aws_subnet.aws_public_subnet_1.id
    route_table_id  = aws_route_table.aws_pub_rt.id 
}

# associates the subnet public subnet to the routing table
resource "aws_route_table_association" "aws_pub_sub_assoc_2" {
    subnet_id       = aws_subnet.aws_public_subnet_2.id
    route_table_id  = aws_route_table.aws_pub_rt.id 
}

# defines the first private subnet of AWS
resource "aws_subnet" "aws_private_subnet_1" {
    vpc_id              = aws_vpc.aws_sstk_vpc.id
    cidr_block          = var.aws_private_subnet_cidr_1
    availability_zone   = var.aws_az_1

    tags = {
        Name = "${var.name}_private_subnet_1"
    }
}

# defines the second private subnet in AWS
resource "aws_subnet" "aws_private_subnet_2" {
    vpc_id              = aws_vpc.aws_sstk_vpc.id
    cidr_block          = var.aws_private_subnet_cidr_2
    availability_zone   = var.aws_az_2

    tags = {
        Name = "${var.name}_private_subnet_2"
    }
}

# defines a load balancer of the AWS application
resource "aws_lb" "aws_alb" {
    name                = "alb"
    internal            = false
    load_balancer_type  = "application"
    security_groups     = [aws_security_group.aws_lb_sg_.id]
    subnets             = [
        aws.aws_public_subnet_1.id,
        aws.aws_public_subnet_2.id
    ]

    tags = {
        Environment = "production"
    }
}

# defines a destiny group para o load balancer
resource "aws_lb_target_group" "aws_app_tg" {
    name        = "AppTargetGroup"
    port        = "80"
    protocol    = "HTTP"
    vpc_id      = "${aws_vpc.aws_sstk_vpc.id}"
}

# defines a listener for the load balancer
resource "aws_lb_listener" "listener" {
    load_balancer_arn   = "${aws_lb.aws_alb.arn}"
    port                = "80"
    protocol            = "HTTP"

    default_action{
        type             = "forward"
        target_group_arn = "${aws_lb_target_group.aws_app_tg_arn}"
    }
}

# defines a security group for a Bastion host
resource "aws_security_group" "aws_bastion_sg"{
    name        = "BastionHostSG"
    description = "Allow SSH"
    vpc_id      = aws_vpc.aws_sstk_vpc.id

    ingress {
        from_port   = "22"
        to_port     = "22"
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# defines a security group for the load balancer
resource "aws_security_group" "aws_lb_sg"{
    name        = "LoadBalancerSG"
    description = "Allow HTTP Access"
    vpc_id      = aws_vpc.aws_sstk_vpc.id

    ingress {
        from_port   = "80"
        to_port     = "80"
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# defines an AWS instance to serve as application server
resource "aws_instance" "sstk-app-server" {
    ami             = "ami-051f8a213df8bc089"
    instance_type   = "t2.micro"
    subnet_id       = aws_subnet.aws_public_subnet_1.id

    security_groups = [
        aws_security_group.aws_bastion_sg.id,
        aws_security_group.aws_lb_sg.id
    ]

    tags = {
        Name = "AppServerInstance"
    }
}