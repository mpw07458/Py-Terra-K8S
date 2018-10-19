variable "client_id" {
  default = "168f8ef0-c532-45f3-af0b-12934bebd639"
}

variable "client_secret" {
  default = "okcDpETZgekzT59euC4I52kjuNmD3SR9WR42G07+SVE="
}

variable "agent_count" {
  default = 4
}

variable "ssh_public_key" {
  default = "~/.ssh/id_rsa.pub"
}

variable "dns_prefix" {
  default = "OpenInno"
}

variable "cluster_name" {
  default = "OpenInnok8s"
}

variable "resource_group_name" {
  default = "RG-Inno-GP-OpenPlatform-AKS"
}

variable "location" {
  default = "West US"
}

variable "nsg_name" {
  default = "OpenInno-nsg"
}

variable "vnet_name" {
  default = "VNT-Inno-GP-OpenPlatform-AKS"
}

variable "subnet_name" {
  default = "SUB-Inno-GP-OpenPlatform-AKSAuto-00"
}

variable "log_workspace_id" {
  default = "5f5ff417-9c32-4b94-93b1-6d793d067428"
}

variable "admin_user_name" {
  default = "OpenInnoAdmin"
}

variable "vnet_address" {
  default = "172.16.0.0/22"
}

variable "subnet_prefix" {
  default = "172.16.0.0/24"
}

variable "service_cidr" {
  default = "172.16.1.0/24"
}

variable "bridge_cidr" {
  default = "172.17.0.1/16"
}

variable "dns_svc_ip" {
  default = "172.16.1.10"
}
