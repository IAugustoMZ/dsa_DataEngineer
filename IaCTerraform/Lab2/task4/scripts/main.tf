module "sstk-ec2_instances" {
  
  source = "./modules/ec2-instances"

  instance_count = 2
  ami_id = "ami-0a0d9cf81c479446a"
  instance_type = "t2.micro"
  subnet_id = "subnet-0739594fa042522f6"
  
}