# main setting file

# variables
variable "region" { default = "us-east-2" }
variable "emr_release_label" {}
variable "emr_main_instance_type" {}
variable "emr_core_instance_type" {}
variable "emr_core_instance_count" {}
variable "project" {}
variable "owner" {}
variable "environment" {}

# locals
locals {
    tags = {
        "owner"         = var.owner
        "project"       = var.project
        "environment"   = var.environment
    }
}

# provider
provider "aws" {
    region = var.region
}

# SSH module
module "ssh" {
    source      = "./ssh"
    project     = var.project
    environment = var.environment
}

# networking module
module "networking" {
    source      = "./network"
    region      = var.region
    tags        = local.tags
}

# Apache Flink module definition
locals {
    configurations_json = jsonencode([
        {
            "Classification": "flink-conf",
            "Properties": {
                "parallelism.default": "2",
                "taskmanager.numberOfTaskSlots": "2",
                "taskmanager.memory.process.size": "2G",
                "jobmanager.memory.process.size": "1G",
                "execution.checkpointing.interval": "180000",
                "execution.checkpointing.mode": "EXACTLY_ONCE"
            }
        }
    ])
}

# EMR module
module "emr" {
    source                          = "./emr"
    project                         = var.project
    environment                     = var.environment
    emr_release_label               = var.emr_release_label
    emr_applications                = ["Hadoop", "Zeppelin", "Flink"]
    emr_main_instance_type          = var.emr_main_instance_type
    emr_core_instance_type          = var.emr_core_instance_type
    emr_core_instance_count         = var.emr_core_instance_count
    configurations                  = local.configurations_json
    key_name                        = module.ssh.deployer_key_name
    vpc_id                          = module.networking.vpc_id
    public_subnet                   = module.networking.public_subnet_2
    additional_security_groups_id   = module.networking.integration_service_security_group_id
    tags                            = local.tags
}

# ouputs
output "emr_main_address" {
    value = module.emr.emr_main_address
}