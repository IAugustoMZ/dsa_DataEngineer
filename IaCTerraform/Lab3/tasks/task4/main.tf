resource "aws_security_group" "sstk_allow_ssh" {

  name = "sstk_allow_ssh"
  description = "SSTK - Security Group to allow SSH - EC2 instance"

  ingress {
    description = "Inbound rule"
    from_port   = 22
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

  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.sstk_allow_ssh.id]

  key_name = "sstk-lab3"

  tags = {
    Name = "SSTK-t4-terraform"
  }

  provisioner "file"{
    source = "./sstk_script.sh"
    destination = "/tmp/sstk_script.sh"

    connection {
      type = "ssh"
      user = "ec2-user"
      private_key = file("./data/sstk-lab3.pem")
      host = self.public_ip
    }
  }

  provisioner "remote-exec" {

        inline = [ "chmod +x /tmp/sstk_script.sh",
                   "/tmp/sstk_script.sh"]
                   
        connection {
            type        = "ssh"
            user        = "ec2-user"
            private_key = file("./data/sstk-lab3.pem")
            host        = self.public_ip
        }
    }
}