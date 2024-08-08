terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.40.0"
    }
  }
}

provider "google" {
  project = "healthcareanalytics-431704"
  region  = "us-central"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "healthcareanalytics-431704-terr-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "healthcare_dataset "
}