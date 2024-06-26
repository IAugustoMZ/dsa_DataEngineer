# create work folders in S3

# python scripts folder
resource "aws_s3_object" "python_scripts" {

    for_each    = fileset("${var.files_bucket}/", "**")
    bucket      = var.bucket_name
    key         = "pipeline/${each.value}"
    source      = "${var.files_bucket}/${each.value}"
    etag        = filemd5("${var.files_bucket}/${each.value}")

}

# raw_data folder
resource "aws_s3_object" "raw_data" {

    for_each    = fileset("${var.files_data}/", "**")
    bucket      = var.bucket_name
    key         = "data/${each.value}"
    source      = "${var.files_data}/${each.value}"
    etag        = filemd5("${var.files_data}/${each.value}")

}

# bash scripts folder
resource "aws_s3_object" "bash_scripts" {

    for_each    = fileset("${var.files_bash}/", "**")
    bucket      = var.bucket_name
    key         = "scripts/${each.value}"
    source      = "${var.files_bash}/${each.value}"
    etag        = filemd5("${var.files_bash}/${each.value}")

}

# processed_data folder
resource "aws_s3_object" "processed_data" {

    bucket      = var.bucket_name
    key         = "data/"
}

# logs folder
resource "aws_s3_object" "logs" {

    bucket      = var.bucket_name
    key         = "logs/"
}

# output folder
resource "aws_s3_object" "output" {

    bucket      = var.bucket_name
    key         = "output/"
}