resource "aws_instance" "sstk_instance" {
  
  ami = "ami-0a0d9cf81c479446a"

  instance_type = var.instance_type

  tags = {
    Name = "SSTK-t1-terraform"
  }

  provisioner "local-exec" {
    command = "echo ${aws_instance.sstk_instance.public_ip} > public_ip.txt"
  }
}