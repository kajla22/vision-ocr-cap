variable "resource_group_name" {
  description = "6517-RG"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "South India"
}

variable "storage_account_name" {
  description = "6517storage1"
  type        = string
}

variable "function_app_name" {
  description = "6517-func-app"
  type        = string
}
