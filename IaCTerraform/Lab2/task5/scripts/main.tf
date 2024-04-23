module "sstk-ec2_instances" {
  
  source = "./modules/ec2-instances"

  instance_count = 2
  ami_id = "ami-0a0d9cf81c479446a"
  instance_type = "t2.micro"
  subnet_id = "subnet-0739594fa042522f6"
  
}

module "sstk_s3_bucket" {
  
  source = "./modules/s3-bucket"
  
  bucket_name = "sstk-bucket-lab2-574973852419"
  tags = { "SSTK" = "Analytics" }
  
}