# provider block
provider "aws"{
    region = "us-east-2"
}

# S3 resource block - to store application files
resource "aws_s3_bucket" "sstk_bucket_flask"{
    bucket = "sstk-flask-bucket-574973852419"

    tags = {
      Name = "SSTK-Flask-Bucket"
      Environment = "Dev"
    }

    # provisioner block
    # provisioner to upload files to bucket
    provisioner "local-exec" {
        command = "${path.module}/upload_to_s3.sh"
    }

    # provisioner to destroy bucket
    provisioner "local-exec" {
        when = destroy
        command = "aws s3 rm s3://sstk-flask-bucket-574973852419 --recursive"
    }
}

# EC2 resource block
resource "aws_instance" "sstk_ml_api" {
    ami = "ami-02bf8ce06a8ed6092"
    instance_type = "t2.micro"
    iam_instance_profile = aws_iam_instance_profile.ec2_s3_profile.name
    vpc_security_group_ids = [aws_security_group.sstk_ml_app_sg.id]
    
    user_data = <<-EOF
                #!/bin/bash
                sudo yum update -y
                sudo yum install -y python3 python3-pip awscli
                sudo pip3 install python-dateutil flask joblib scikit-learn numpy pandas scipy gunicorn
                sudo mkdir /sstk_ml_app
                sudo /usr/bin/python3 -m awscli s3 sync s3://sstk-flask-bucket-574973852419 /sstk_ml_app
                cd /sstk_ml_app
                nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app &
                EOF

    tags = {
        Name = "SSTK-ML-API"
    }
}

# create security group for EC2 instance
resource "aws_security_group" "sstk_ml_app_sg" {
    name        = "sstk_ml_app_sg"

    description = "Security group for flask app in EC2"

    # ingress rules
    ingress {
        description = "Rule 1"
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"] 
    }

    ingress {
        description = "Rule 2"
        from_port   = 5000
        to_port     = 5000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        description = "Rule 3"
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # egress rules
    egress {
        from_port   = 0
        to_port     = 65535
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# create IAM role for EC2 instance
resource "aws_iam_role" "ec2_s3_access_role" {
    name = "ec2_s3_access_role"
    
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {

                Effect = "Allow",
                Principal = {
                    Service = "ec2.amazonaws.com"
                },
                Action = "sts:AssumeRole"
            }
        ]

    })
}

# create IAM policy for S3 access
resource "aws_iam_role_policy" "s3_access_policy" {
    name = "s3_access_policy"
    role = aws_iam_role.ec2_s3_access_role.id

    policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Action = [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                Resource = [
                    "${aws_s3_bucket.sstk_bucket_flask.arn}",
                    "${aws_s3_bucket.sstk_bucket_flask.arn}/*"
                ]
            }
        ]
    })
}

# create IAM instance profile
resource "aws_iam_instance_profile" "ec2_s3_profile" {
    name = "ec2_s3_profile"
    role = aws_iam_role.ec2_s3_access_role.name
}