provider "aws" {
  region = "us-east-2"
}

resource "aws_security_group" "sstk_allow_ssh" {

  name = "sstk_allow_ssh"
  description = "SSTK - Security Group to allow SSH - EC2 instance"

  ingress {
    description = "Inbound rule"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Outbound rule"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "sstk_instance" {

  # defining the for
  count = 3

  # check if the ami is the right one
  ami = var.ami_id[count.index] != "ami-0a0d9cf81c479446a" ? "ami-0a0d9cf81c479446a" : var.ami_id[count.index]

  # validate if the instance type is the right one
  instance_type = var.instance_type[count.index] != "t2.micro" ? "t2.micro" : var.instance_type[count.index]

  vpc_security_group_ids = [aws_security_group.sstk_allow_ssh.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              sudo bash -c 'echo <h1>Welcome to Server ${count.index+1}</h1> > /var/www/html/index.html'
              EOF

  tags ={
    Name =  "SSTK-t5-terraform-${count.index+1}"
  }
}