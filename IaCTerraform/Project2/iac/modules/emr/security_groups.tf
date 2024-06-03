# security groups

# security group for the main node of EMR
resource "aws_security_group" "main_security_group" {
  
  # name of the security group
  name = "sstk-emr-main-security-group-p2"

  # description of the security group
  description = "Allow inbound traffic for EMR main node"

  # option to revoke security rules when deleting security group
  revoke_rules_on_delete = true

  # ingress rules to allow SSH traffic
  ingress {
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # egress rules to allow traffic to the internet
  egress {
    from_port     = "0"
    to_port       = "0"
    protocol      = "-1"
    cidr_blocks   = ["0.0.0.0/0"]
  }
}

# definition of security group for the core nodes of the EMR
resource "aws_security_group" "core_security_group" {

    # security group name
    name = "sstk-emr-core-security-group-p2"

    # security group description
    description = "Allow inbound traffic for EMR core nodes"

    # option to revoke security rules when deleting security group
    revoke_rules_on_delete = true

    # ingress rule to allow all traffic inside the security group
    ingress {
        from_port   = "0"
        to_port     = "0"
        protocol    = "-1"
        self        = true
    }

    # egress rule to allow all outbound traffic
    egress {
        from_port     = "0"
        to_port       = "0"
        protocol      = "-1"
        cidr_blocks   = ["0.0.0.0/0"]
    }
}