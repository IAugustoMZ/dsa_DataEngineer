# create work folders in S3

# python scripts folder
resource "aws_s3_obejct" "python_scripts" {

    for_each    = fileset("${var.files_bucket}/", "**")
    bucket      = var.bucket_name
    key         = "pipeline/${each.value}"
    source      = "${var.files_bucket}/${each.value}"
    etag        = filemd5("${var.files_bucket}/${each.value}")

}

# raw_data folder
resource "aws_s3_obejct" "raw_data" {

    for_each    = fileset("${var.files_data}/", "**")
    bucket      = var.bucket_name
    key         = "data/${each.value}"
    source      = "${var.files_data}/${each.value}"
    etag        = filemd5("${var.files_data}/${each.value}")

}

# bash scripts folder
resource "aws_s3_obejct" "bash_scripts" {

    for_each    = fileset("${var.files_bash}/", "**")
    bucket      = var.bucket_name
    key         = "data/${each.value}"
    source      = "${var.files_bash}/${each.value}"
    etag        = filemd5("${var.files_bash}/${each.value}")

}

# processed_data folder
resource "aws_s3_obejct" "processed_data" {

    bucket      = var.bucket_name
    key         = "data/"
}

# logs folder
resource "aws_s3_obejct" "logs" {

    bucket      = var.bucket_name
    key         = "logs/"
}

# output folder
resource "aws_s3_obejct" "output" {

    bucket      = var.bucket_name
    key         = "output/"
}