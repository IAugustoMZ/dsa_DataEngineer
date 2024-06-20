# configuration of the job

variable "job_name" {
  description   = "Name of the Databricks job"
  type          = string
  default       = "SSTK Databricks Job"
}

variable "task_key" {
  description   = "Key of the task to run"
  type          = string
  default       = "sstk_p5_task"
}

resource "databricks_job" "sstk_job" {
  name          = var.job_name
  task {
    task_key = var.task_key
    existing_cluster_id = databricks_cluster.sstk_cluster.id

    notebook_task {
        notebook_path = databricks_notebook.sstk_notebook.path
    }
  }

  email_notifications {
    on_success = [ data.databricks_current_user.me.user_name ]
    on_failure = [ data.databricks_current_user.me.user_name ]
  }
}

output "job_url" {
  value = databricks_job.sstk_job.url
}