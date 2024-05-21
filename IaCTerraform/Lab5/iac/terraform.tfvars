project_name                = "sstk-lab5-dsa"
environment                 = "dev"
container_port              = "80" 
vpc_cidr_block              = "10.0.0.0/16"
avail_zone1                 = "us-east-2a"
avail_zone2                 = "us-east-2b"
public_subnet_1_cidr_block  = "10.0.1.0/24"
public_subnet_2_cidr_block  = "10.0.2.0/24"
private_subnet_1_cidr_block = "10.0.3.0/24"
alb_sg_port                 = "80"
cpu                         = "256"
memory                      = "512"
docker_image_name           = "nginx:latest"
s3_env_vars_file_arn        = "arn:aws:s3:::sstk-lab5-574973852419/vars.env"
awslogs_region              = "us-east-2"
desired_count               = "1"
health_check_path           = "/" 