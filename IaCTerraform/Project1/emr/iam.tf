# AWS EMR service, profile and role
resource "aws_iam_role" "sstk-emr-service-role" {
    name = "${var.project}-${var.environment}-emr-service-role"
    tags = var.tags
    assume_role_policy = <<EOF
    {
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "elasticmapreduce.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    EOF
}

# service role policy
resource "aws_iam_role_policy_attachment" "sstk-emr-service-role-policy" {
    role = aws_iam_role.sstk-emr-service-role.id
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

# AWS EC2 IAM service role
resource "aws_iam_role" "sstk_emr_profile_role" {
    name = "${var.project}-${var.environment}-emr-profile-role"
    tags = var.tags
    
    assume_role_policy = <<EOF
    {
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    EOF
}

# policy of profile role
resource "aws_iam_role_policy_attachment" "sstk_emr_profile_role_policy" {
    role = aws_iam_role.sstk_emr_profile_role.id
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
}

# IAM instance profile
resource "aws_iam_instance_profile" "sstk_ec2_emr_instance_profile" {
    name = "${var.project}-${var.environment}-emr-instance-profile"
    role = aws_iam_role.sstk_emr_profile_role.name
}