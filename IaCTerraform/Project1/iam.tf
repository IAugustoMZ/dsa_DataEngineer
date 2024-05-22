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

