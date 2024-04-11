provider "aws" {
  region = var.region
}

resource "aws_instance" "sstk-ec2-1" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnets[0]
  tags = {
    Name = "SSTK - EC2 Instance - 1"
  }
}

resource "aws_instance" "sstk-ec2-2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnets[1]
  tags = {
    Name = "SSTK - EC2 Instance - 2"
  }
}