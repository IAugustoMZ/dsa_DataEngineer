# security groups

# define security group for the main node of EMR
resource "aws_security_group" "sstk_emr_main_security_group" {

    # name
    name = "${var.project}-${var.environment}-emr-main-sg"

    # description
    description = "Allows inbound traffic to the main node of EMR"

    # vpc id
    vpc_id = var.vpc_id

    # tags
    tags = var.tags

    # revoke all rules by default
    revoke_rules_on_delete = true

    # ingress rules
    ingress {
        from_port   = "22"
        to_port     = "22"
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # egress rules
    egress {
        from_port   = "0"
        to_port     = "0"
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# define security group for the core node of EMR
resource "aws_security_group" "sstk_emr_core_security_group" {

    # name
    name = "${var.project}-${var.environment}-emr-core-sg"

    # description
    description = "Allows outbound traffic from the core nodes of EMR"

    # vpc id
    vpc_id = var.vpc_id

    # tags
    tags = var.tags

    # revoke all rules by default
    revoke_rules_on_delete = true

    # ingress rules
    ingress {
        from_port   = "0"
        to_port     = "0"
        protocol    = "-1"
        self = true
    }

    # egress rules
    egress {
        from_port   = "0"
        to_port     = "0"
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
