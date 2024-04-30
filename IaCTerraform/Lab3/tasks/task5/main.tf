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
  
  ami = "ami-0a0d9cf81c479446a"

  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.sstk_allow_ssh.id]

  key_name = "sstk-lab3"

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              sudo bash -c 'echo This is the fourth web server from SSTK with Terraform > /var/www/html/index.html'
              EOF

  tags = {
    Name = "SSTK-t5-terraform"
  }
}