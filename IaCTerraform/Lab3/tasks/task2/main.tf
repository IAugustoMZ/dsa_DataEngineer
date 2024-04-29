resource "aws_instance" "sstk_instance" {
  
  ami = "ami-0a0d9cf81c479446a"

  instance_type = var.instance_type

  key_name = "sstk-lab3"

  tags = {
    Name = "SSTK-t1-terraform"
  }

  provisioner "remote-exec" {

        inline = [  "sudo yum update -y",
                    "sudo yum install -y httpd",
                    "sudo systemctl start httpd",
                    "sudo bash -c 'echo This is the first Sistek Analytics Serveer with Terraform > /var/www/html/index.html'",]

        connection {
            type        = "ssh"
            user        = "ec2-user"
            private_key = file("./data/sstk-lab3.pem")
            host        = self.public_ip
        }
    }
}