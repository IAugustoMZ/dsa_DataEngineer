# S3 objects variables

variable "bucket_name" {
    type        = string
    description = "Bucket Name"
}

variable "files_bucket" {
    type        = string
    description = "Source folder to store Python scripts for preprocessing and training"
}

variable "files_data" {
    type        = string
    description = "Source folder to store data for preprocessing and training"
}

variable "files_bash" {
    type        = string
    description = "Source folder to store bash scripts for preprocessing and training"
}