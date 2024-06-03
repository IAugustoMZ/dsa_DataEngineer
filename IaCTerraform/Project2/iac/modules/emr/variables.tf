# variables EMR

variable "name_emr" {
    type        = string
    description = "Name of the EMR cluster"
}

variable "name_bucket" {
    type        = string
    description = "Name of the bucket"
}

variable "instance_profile" {}

variable "service_role" {}