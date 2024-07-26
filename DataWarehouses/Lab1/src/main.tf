provider "google" {
    project = "modeling-dw-dsa"
    region  = "us-west1"
}

resource "google_bigquery_dataset" "sstk_dw_lab1" {
    dataset_id      = "sstk_dw_lab1"
    friendly_name   = "Database for Lab1 - DataWarehouses"
    description     = "This dataset is used for Lab1 of the DataWarehouses course"
    location        = "US"
}

