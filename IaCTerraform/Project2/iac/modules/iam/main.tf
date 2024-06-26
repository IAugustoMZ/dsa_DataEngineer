# IAM resources configuration

# IAM role for EMR services
resource "aws_iam_role" "iam_emr_service_role" {
  name = "iam_emr_service_role"

  description = "Role for EMR services"

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
  ]

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

# IAM role for EC2 instance profiles
resource "aws_iam_role" "iam_emr_profile_role" {
    name = "iam_emr_profile_role"
    description = "Role for EC2 instance profiles"
    
    managed_policy_arns = [
        "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
    ]

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

# EC2 instance profile
resource "aws_iam_instance_profile" "emr_instance_profile" {
  name = "emr_instance_profile"
  role = aws_iam_role.iam_emr_profile_role.name
}