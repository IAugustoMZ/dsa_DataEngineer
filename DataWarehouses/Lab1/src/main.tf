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

resource "google_bigquery_table" "production_database" {
    deletion_protection = false
    dataset_id          = google_bigquery_dataset.sstk_dw_lab1.dataset_id
    table_id            = "production_database"

    schema = jsonencode([
        {
            "name": "record_date",
            "type": "TIMESTAMP",
            "mode": "REQUIRED"
        },
        {
            "name": "volume_produced",
            "type": "INTEGER",
            "mode": "REQUIRED"
        },
        {
            "name": "sku",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "production_line",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "defective_volume",
            "type": "INTEGER",
            "mode": "REQUIRED"
        },
        {
            "name": "defect_description",
            "type": "STRING",
            "mode": "NULLABLE"
        },
        {
            "name": "downtime_minutes",
            "type": "INTEGER",
            "mode": "REQUIRED"
        },
        {
            "name": "downtime_reason",
            "type": "STRING",
            "mode": "NULLABLE"
        },
        {
            "name": "production_shift",
            "type": "STRING",
            "mode": "REQUIRED"
        }
    ])
}

resource "google_bigquery_table" "product_table" {
    deletion_protection = false
    dataset_id          = google_bigquery_dataset.sstk_dw_lab1.dataset_id
    table_id            = "product_table"

    schema = jsonencode([
        {
            "name": "sku",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "product_name",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "cost",
            "type": "FLOAT",
            "mode": "REQUIRED"
        }
    ])
}

resource "random_string" "random_id" {
    length  = 8
    special = false
    upper   = false
}

resource "google_bigquery_job" "job_sql_1"{
    job_id = "dsa_job_${random_string.random_id.result}_1"

    labels = {
        "sstk_job" = "sstk_sql_1"
    }

    load {
      source_uris = [
        "gs://modeling-dw-dsa/lab1/production_data_2023.csv"
      ]

      destination_table {
        project_id = google_bigquery_table.production_database.project
        dataset_id = google_bigquery_table.production_database.dataset_id
        table_id   = google_bigquery_table.production_database.table_id
      }

      skip_leading_rows = 1
      schema_update_options = [ "ALLOW_FIELD_ADDITION", "ALLOW_FIELD_RELAXATION" ]
      write_disposition = "WRITE_APPEND"
      autodetect = true
    }
}

resource "google_bigquery_job" "job_sql_2"{
    job_id = "dsa_job_${random_string.random_id.result}_2"

    labels = {
        "sstk_job" = "sstk_sql_2"
    }

    load {
      source_uris = [
        "gs://modeling-dw-dsa/lab1/sku_product_data_2023.csv"
      ]

      destination_table {
        project_id = google_bigquery_table.product_table.project
        dataset_id = google_bigquery_table.product_table.dataset_id
        table_id   = google_bigquery_table.product_table.table_id
      }

      skip_leading_rows = 1
      schema_update_options = [ "ALLOW_FIELD_ADDITION", "ALLOW_FIELD_RELAXATION" ]
      write_disposition = "WRITE_APPEND"
      autodetect = true
    }
}