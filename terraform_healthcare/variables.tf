variable "project" {
  description = "Project"
  default     = "healthcareanalytics-431704"
}

variable "region" {
  description = "Region"
  default     = "us-central"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "health_care_dataset_name" {
  description = "BigQuery Dataset Name for Health Care"
  default     = "health_care"
}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
  default     = "healthcareanalytics-431704-terr-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "service_account_email" {
  description = "Service account email that will have BigQuery Data Editor and Data Viewer roles"
  type        = string
}
