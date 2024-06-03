# variable definition script
variable "name_bucket" {
    type        = string
    description = "Bucket Name"
}

variable "name_bucket_state" {
    type        = string
    description = "Name of bucket to store Terraform state file"
}

variable "versioning_bucket" {
    type        = string
    description = "Defines if the bucket will have versioning enabled"
}

variable "files_bucket" {
    type        = string
    description = "Source folder to store Python scripts for preprocessing and training"
    default     = "./pipeline"
}

variable "files_data" {
    type        = string
    description = "Source folder to store data for preprocessing and training"
    default     = "./data"
}

variable "files_bash" {
    type        = string
    description = "Source folder to store bash scripts for preprocessing and training"
    default     = "./scripts"
}

variable "name_emr" {
    type        = string
    description = "Name of the EMR cluster"
}

variable "region" {
    type        = string
    description = "AWS region"
    default     = "us-east-2"
}