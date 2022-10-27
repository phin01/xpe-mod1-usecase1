variable "base_bucket_name" {
  default = "datalake-edc-usecase1-tf"
}

variable "environment" {
  default = "dev"
}

variable "aws_account" {
  default = "1234567"
}

variable "aws_region" {
  default = "us-east-1"
}

variable "lambda_function_name" {
  default = "IGTIexecutaEMR"
}