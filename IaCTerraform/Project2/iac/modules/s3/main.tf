# storage module with Amazon S3 bucket
resource "aws_s3_bucket" "create_bucket" {
    bucket = var.name_bucket

    force_destroy = true

    tags = {
      Name          = "Bucket to be used along with AWS EMR"
      Environment   = "Development"
    }
}

# bucket versioning
resource "aws_s3_bucket_versioning" "versioning_bucket" {
    bucket = aws_s3_bucket.create_bucket.id

    versioning_configuration { status = var.versioning_bucket }

    depends_on = [ aws_s3_bucket.create_bucket ]
}

# blocks public access
resource "aws_s3_bucket_public_access_block" "sstk-ml-safety-example" {

    bucket = aws_s3_bucket.create_bucket.id

    block_public_policy = false
    restrict_public_buckets = false
}

# S3 Objects module - to create folders inside the S3
module "s3_object" {
    source          = "./s3_objects"
    bucket_name     = aws_s3_bucket.create_bucket.bucket
    files_bucket    = var.files_bucket
    files_data      = var.files_data
    files_bash      = var.files_bash
}