provider "aws" {
    region = "us-east-2"
}

resource "aws_instance" "sstk-lab1" {
    ami             = "ami-0a0d9cf81c479446a"  # imagem da máquina (AMI)
    instance_type   = "t2.micro"

    tags = {
        Name = "sstk-lab1-terraform"
    }
}