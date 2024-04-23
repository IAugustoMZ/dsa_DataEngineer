resource "aws_instance" "sstk-instance" {
  count         = var.instance_count
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id

  tags = {
    Name = "sstk-instance-${count.index}"
  }
}