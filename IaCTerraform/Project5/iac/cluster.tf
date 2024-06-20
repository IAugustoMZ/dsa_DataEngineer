# configuration of Databricks cluster
variable "cluster_name" {
  description   = "Name of the Databricks cluster"
  type          = string
  default       = "SSTK Databricks Cluster"
}

variable "cluster_auto_termination_minutes" {
  description   = "Number of minutes after which the cluster will be automatically terminated"
  type          = number
  default       = 60
}

variable "cluster_num_workers" {
  description   = "Number of workers in the cluster"
  type          = number
  default       = 1
}

# create a cluster with the minimum requirements allowed
data "databricks_node_type" "smallest" {
  local_disk = true
}

# use the most recent Databricks runtime
# Long Term Support (LTS) version
data "databricks_spark_version" "latest_lts" {
    long_term_support = true
}

resource "databricks_cluster" "sstk_cluster" {
    cluster_name            = var.cluster_name
    node_type_id            = data.databricks_node_type.smallest.id
    spark_version           = data.databricks_spark_version.latest_lts.id
    num_workers             = var.cluster_num_workers
    autotermination_minutes = var.cluster_auto_termination_minutes
}

output "cluster_url" {
    value = databricks_cluster.sstk_cluster.cluster_url
}