# configuration of the notebook

# get information about the user
data "databricks_current_user" "me" {}

variable "notebook_subdirectory" {
  description   = "Subdirectory in which to create the notebook"
  type          = string
  default       = "SSTK-Project5"
}

variable "notebook_file_name" {
  description   = "Name of the notebook file"
  type          = string
}

variable "notebook_language" {
  description   = "Programming language of the notebook"
  type          = string
}

resource "databricks_notebook" "sstk_notebook" {
  path           = "${data.databricks_current_user.me.home}/${var.notebook_subdirectory}/${var.notebook_file_name}"
  language       = var.notebook_language
  source         = "./${var.notebook_file_name}"
}

output "notebook_url" {
  value = databricks_notebook.sstk_notebook.path
}