# provisioning of EMR cluster

# variables
variable "project" { }
variable "environment" { }
variable "tags" { }
variable "key_name" { }
variable "vpc_id" { }
variable "public_subnet" { }
variable "additional_security_groups_id" { }
variable "emr_release_label" { }
variable "emr_applications" { }
variable "emr_main_instance_type" { }
variable "emr_core_instance_type" { }
variable "emr_core_instance_count" { }
variable "core_instance_ebs_volume_size" { default = "80" }
variable "security_configuration_name" { default = null }
variable "log_uri" { default = "s3://sstk-project1-<account-id>" }
variable "configurations" { default = null }
variable "steps" {
    type = list(object({
        name                = string
        action_on_failure   = string
        hadoop_jar_step     = list(object(
            {
                jar         = string
                main_class  = string
                args        = list(string)
                properties  = map(string)
            }
        ))
    }
    ))
    default = null
}
variable "bootstrap_actions" {
    type = set(object(
        {
            name = string
            path = string
            args = list(string)
        }
    ))
    default = []
}
variable "kerberos_attributes" {
    type = set(object(
        {
            kdc_admin_password  = string
            realm               = string
        }
    ))
    default = []
}

# create the resources
resource "aws_emr_cluster" "sstk-emr-cluster" {
    name                    = "${var.project}-${var.environment}-emr-cluster"
    release_label           = var.emr_release_label
    applications            = var.emr_applications
    security_configuration  = var.security_configuration_name
    service_role            = aws_iam_role.sstk-emr-service-role.arn
    log_uri                 = var.log_uri
    configurations          = var.configurations
    step                    = var.steps
    tags                    = var.tags

    # configuration for the master
    master_instance_group {
        instance_type       = var.emr_main_instance_type
        instance_count      = "1"
    }

    # configuration for the core
    core_instance_group {
        instance_type       = var.emr_core_instance_type
        instance_count      = var.emr_core_instance_count
        ebs_config {
            size     = var.core_instance_ebs_volume_size
            type     = "gp2"
            volumes_per_instance = 1
        }
    }

    # configuration of the ec2 attributes
    ec2_attributes {
        key_name                            = var.key_name
        subnet_id                           = var.public_subnet
        instance_profile                    = aws_iam_instance_profile.sstk-ec2-instance-profile.arn
        emr_managed_master_security_group   = aws_security_group.main_security_group.id
        emr_managed_slave_security_group    = aws_security_group.core_security_group.id
        additional_master_security_groups   = var.additional_security_groups_id
        additional_slave_security_groups    = var.additional_security_groups_id 
    }

    dynamic "bootstrap_action" {
        for_each = var.bootstrap_actions
        content {
            name = bootstrap_action.value["name"]
            path = bootstrap_action.value["path"]
            args = bootstrap_action.value["args"]
        }
    }

    dynamic "kerberos_attributes" {
        for_each                = var.kerberos_attributes
        content {
            kdc_admin_password  = kerberos_attributes.value["kdc_admin_password"]
            realm               = kerberos_attributes.value["realm"]
        }
    }

    lifecycle {
        ignore_changes = [
            step,
        ]
    }
}

# getting the service DNS
output "emr_main_address" {
    value = aws_emr_cluster.sstk-emr-cluster.master_public_dns
}