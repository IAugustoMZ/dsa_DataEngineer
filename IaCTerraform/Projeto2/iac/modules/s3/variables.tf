# S3 module variables
variable "name_bucket" {
  description = "Name of the bucket to be created"
  type        = string
}

variable "versioning_bucket" {
  description = "Enable or disable versioning for the bucket"
  type        = string
}

variable "files_bucket" {
  description = "Folder of Python files to be uploaded to the bucket"
  type        = string
}

variable "files_data" {
  description = "Folder of data files to be uploaded to the bucket"
  type        = string
}

variable "files_bash" {
  description = "Folder of bash files to be uploaded to the bucket"
  type        = string
}