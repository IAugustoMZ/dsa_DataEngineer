resource "aws_s3_bucket" "sstk_bucket" {
  bucket = var.bucket_name
  tags   = var.tags 
}