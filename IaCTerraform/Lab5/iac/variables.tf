variable "project_name" {}
variable "environment" {}
variable "container_port" {}
variable "health_check_path" { default = "/" }
variable "cpu" {}
variable "memory" {}
variable "aws_account_id" { default = "574973852419" }
variable "docker_image_name" {}
variable "s3_env_vars_file_arn" {}
variable "awslogs_region" {}
variable "desired_count" {}
variable "vpc_cidr_block" {}
variable "avail_zone1" {}
variable "avail_zone2" {}
variable "public_subnet_1_cidr_block" {}
variable "public_subnet_2_cidr_block" {}
variable "private_subnet_1_cidr_block" {}
variable "alb_sg_port" {}

